import pytest
from django.urls import reverse
from garden.models import (WateringStation, _default_moisture_threshold, _default_status,
                           _default_watering_duration)
from garden.utils import build_duration_string, derive_duration_string
from tests.assertions import assert_image_files_equal

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.garden_list_page import GardenListPage
from .pages.garden_update_page import GardenUpdatePage
from .pages.watering_station_detail_page import WateringStationDetailPage
from .pages.watering_station_update_page import WateringStationUpdatePage


class TestGardenModification(Base):
    @pytest.fixture(autouse=True)
    def setup(self, user_factory, garden_factory, test_password, live_server, use_tmp_static_dir):
        self.email = 'email@demo.com'
        self.user = user_factory(email=self.email, password=test_password)
        self.num_watering_stations = 10
        self.garden = garden_factory(owner=self.user,
                                     watering_stations=self.num_watering_stations,
                                     watering_stations__defaults=True)
        self.url = live_server.url + reverse('garden-detail', kwargs={'pk': self.garden.pk})
        self.create_authenticated_session(self.user, live_server)

    @pytest.mark.django_db
    def test_a_user_can_modify_their_garden(self):
        self.driver.get(self.url)
        garden_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(garden_page)

        # the user clicks the edit button and is taken to update garden page
        garden_page.edit_button.click()
        update_gpage = GardenUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_gpage)

        # the user sees a form that lets them change the name of the garden, upload a different picture for the garden,
        # and delete the garden. They enter invalid data and try to submit the form, but they see errors.
        update_gpage.update_garden(update_frequency=-1)
        self.wait_for_form_error('error_1_id_update_frequency')

        # they then enter valid information and submit the form
        new_garden_name = 'My new garden name'
        new_garden_image = 'test_garden_image.png'
        new_update_frequency = '10:00'
        update_gpage.update_garden(
            submit=False,
            name=new_garden_name,
            update_frequency=new_update_frequency,
            image=new_garden_image
        )
        self.perform_image_crop(update_gpage, new_garden_image)
        update_gpage.submit_button.click()

        # goes back to the garden detail page where they see the new name and image
        update_gpage.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(garden_page)
        assert garden_page.get_garden_name() == new_garden_name
        assert_image_files_equal(garden_page.get_garden_image_src(), new_garden_image)

        # the user the clicks edit again and is taken back to the update garden page, where they see their new data
        # prefilled in the form
        garden_page.edit_button.click()
        self.wait_for_page_to_be_loaded(update_gpage)
        update_gpage.assert_form_has_values(
            name=new_garden_name, update_frequency=new_update_frequency, image=new_garden_image)

        # the user then deletes the garden
        self.perform_delete_modal_checks(update_gpage)

        # they are then redirected back to the garden list page where they see no gardens
        list_gpage = GardenListPage(self.driver)
        self.wait_for_page_to_be_loaded(list_gpage)
        assert list_gpage.get_number_of_gardens() == 0

    @pytest.mark.django_db
    def test_user_can_modify_their_gardens_watering_stations(self):
        # a user goes to a garden detail page
        self.driver.get(self.url)
        garden_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(garden_page)

        # the user sees information about the garden
        assert garden_page.is_displaying_info_for_garden(self.garden)

        # they see a table, where each row corresponds to a watering station in the garden and the header of the table
        # displays the field names of the watering_stations
        self.assert_watering_station_table_contains_correct_headers(garden_page)

        # the user also notices that the row display some information about the watering station
        selected_watering_station = 1
        assert str(selected_watering_station) == garden_page.get_watering_station_field_value(
            selected_watering_station, 'Watering Station Number')
        table_data = garden_page.get_water_station_data_from_table(selected_watering_station)
        table_data['status'] = self.ws_status_to_bool(table_data['status'])

        # they click a watering station link and are taken to the watering station detail page.
        garden_page.watering_station = selected_watering_station
        detail_ws_page = WateringStationDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_ws_page)

        # the user sees that the watering station has the same information as on the table in the previous page
        self.assert_watering_station_has_values(table_data, detail_ws_page)
        assert detail_ws_page.get_ws_idx() == str(selected_watering_station)

        # they see an edit button on the page and click it.
        detail_ws_page.edit_button.click()

        # they are taken to a page with a form that allows them to edit the configurations of the watering station.
        # The user notices that the values in the form are the same as in the previous pages
        update_ws_page = WateringStationUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_ws_page)
        self.assert_update_watering_station_form_has_values(table_data, update_ws_page)
        self.assert_update_watering_station_form_has_default_values(update_ws_page)

        # the user tries to enter invalid info, but the form renders errors
        moisture_threshold = -1
        watering_duration = -1
        update_ws_page.update_info(
            moisture_threshold=moisture_threshold,
            watering_duration=watering_duration
        )
        self.wait_for_form_error('error_1_id_moisture_threshold')
        self.wait_for_form_error('error_1_id_watering_duration')

        # the user then changes these values and submits the form
        ws_status = not table_data['status']
        plant_type = 'lettuce'
        moisture_threshold = '80'
        watering_duration = build_duration_string(minutes=10, seconds=2)
        image = 'test_lettuce_image.png'
        update_ws_page.update_info(ws_status, plant_type, moisture_threshold,
                                   watering_duration, image, self.perform_image_crop)

        # they then go back to the garden detail view and sees that the changes have been persisted in the table
        update_ws_page.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(garden_page)
        table_data = garden_page.get_water_station_data_from_table(selected_watering_station)
        table_data['status'] = self.ws_status_to_bool(table_data['status'])
        assert ws_status == table_data['status']
        assert plant_type == table_data['plant_type']
        assert moisture_threshold == table_data['moisture_threshold']
        assert watering_duration == table_data['watering_duration']

        # the user then selects a different watering station page
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(detail_ws_page)
        self.assert_watering_station_has_default_values(detail_ws_page)

        # they then use the navbar to go directly to the watering station that they had edited and see that their
        # configurations have persisted on both the detail and update pages
        update_ws_page.go_to_watering_station_page(selected_watering_station)
        self.assert_watering_station_has_values(table_data, detail_ws_page)
        detail_ws_page.edit_button.click()
        self.wait_for_page_to_be_loaded(update_ws_page)
        self.assert_update_watering_station_form_has_values(table_data, update_ws_page)

        # the user then goes back to the garden detail page and clicks on the add watering station button and sees
        # that the page now displays and extra watering station in the table
        update_ws_page.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(garden_page)
        garden_page.add_watering_station_button.click()
        assert garden_page.get_number_watering_stations() == self.num_watering_stations + 1

        # the user then clicks the deactivate all button and all watering stations in the table are deactivated
        garden_page.deactivate_button.click()
        for i in range(1, self.num_watering_stations + 1):
            status = garden_page.get_watering_station_field_value(i, 'Status')
            assert not self.ws_status_to_bool(status)

        # the user then goes to watering_station page and deletes the watering station
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(detail_ws_page)
        detail_ws_page.edit_button.click()
        self.wait_for_page_to_be_loaded(update_ws_page)
        self.perform_delete_modal_checks(update_ws_page)

        # They are then redirected back to the garden detail page, where they see 1 less watering station
        self.wait_for_page_to_be_loaded(garden_page)
        assert garden_page.get_number_watering_stations() == self.num_watering_stations

    def assert_watering_station_has_default_values(self, detail_ws_page):
        data = self._get_default_watering_station_data()
        self.assert_watering_station_has_values(data, detail_ws_page)

    def assert_watering_station_has_values(self, data, detail_ws_page):
        assert data['status'] == self.ws_status_to_bool(detail_ws_page.get_status())
        assert data['plant_type'] == detail_ws_page.get_plant_type()
        assert data['moisture_threshold'] == detail_ws_page.get_moisture_threshold()
        assert data['watering_duration'] == detail_ws_page.get_watering_duration()

    def assert_update_watering_station_form_has_default_values(self, update_ws_page):
        data = self._get_default_watering_station_data()
        self.assert_update_watering_station_form_has_values(data, update_ws_page)

    def assert_update_watering_station_form_has_values(self, data, update_ws_page):
        for key, value in data.items():
            assert getattr(update_ws_page, key) == value

    def assert_watering_station_table_contains_correct_headers(self, garden_page):
        assert garden_page.get_number_watering_stations() == self.garden.watering_stations.count()
        assert garden_page.field_is_in_watering_station_table('Watering Station Number')
        assert garden_page.field_is_in_watering_station_table('Status')
        assert garden_page.field_is_in_watering_station_table('Plant Type')
        assert garden_page.field_is_in_watering_station_table('Moisture Threshold')
        assert garden_page.field_is_in_watering_station_table('Watering Duration')

    def perform_delete_modal_checks(self, page):
        # the user clicks the delete button on the page. They see a modal pop up asking them to confirm their decision.
        page.delete_button.click()
        self.wait_for_modal_to_be_visible(page.modal_id)

        # the user decides not to delete the watering station and clicks cancel and the modal disappears. They then
        # quickly change their mind and proceed to delete the watering station.
        page.cancel_button.click()
        self.wait_for_model_to_disappear(page.modal_id)
        page.delete_button.click()
        self.wait_for_modal_to_be_visible(page.modal_id)
        page.confirm_delete_button.click()

    def _get_default_watering_station_data(self):
        return {
            'status': _default_status(),
            'plant_type': '',
            'moisture_threshold': str(_default_moisture_threshold()),
            'watering_duration': derive_duration_string(_default_watering_duration())
        }

    def ws_status_to_bool(self, status):
        return True if status == WateringStation.ACTIVE_STATUS_STR else False
