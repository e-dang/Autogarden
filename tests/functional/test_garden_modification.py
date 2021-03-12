import pytest
from django.urls import reverse
from garden.formatters import WateringStationFormatter
from garden.utils import build_duration_string
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
        self.garden.refresh_from_db()
        assert garden_page.is_displaying_info_for_garden(self.garden)

        # they see a table, where each row corresponds to a watering station in the garden and the header of the table
        # displays the field names of the watering_stations
        self.assert_watering_station_table_contains_correct_headers(garden_page)

        # the user also notices that the row display some information about the watering station
        selected_watering_station = 1
        watering_station = self.garden.get_watering_station_at_idx(selected_watering_station - 1)
        assert garden_page.is_table_row_displaying_data_for_watering_station(
            selected_watering_station, watering_station)

        # they click a watering station link and are taken to the watering station detail page.
        garden_page.watering_station = selected_watering_station
        detail_ws_page = WateringStationDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_ws_page)

        # the user sees that the watering station has the same information as on the table in the previous page
        assert detail_ws_page.is_displaying_data_for_watering_station(watering_station)

        # they see an edit button on the page and click it.
        detail_ws_page.edit_button.click()

        # they are taken to a page with a form that allows them to edit the configurations of the watering station.
        # The user notices that the values in the form are from the same watering station
        update_ws_page = WateringStationUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_ws_page)
        assert update_ws_page.form_has_values_from_watering_station(watering_station)

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
        ws_status = not watering_station.status
        plant_type = 'lettuce'
        moisture_threshold = '80'
        watering_duration = build_duration_string(minutes=10, seconds=2)
        image = 'test_lettuce_image.png'
        update_ws_page.update_info(ws_status, plant_type, moisture_threshold,
                                   watering_duration, image, self.perform_image_crop)
        watering_station.refresh_from_db()

        # they then go back to the garden detail view and sees that the changes have been persisted in the table
        update_ws_page.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(garden_page)
        assert garden_page.is_table_row_displaying_data_for_watering_station(
            selected_watering_station, watering_station)

        # the user then selects a different watering station page
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(detail_ws_page)

        # they then use the navbar to go directly to the watering station that they had edited and see that their
        # configurations have persisted on both the detail and update pages
        update_ws_page.go_to_watering_station_page(selected_watering_station)
        detail_ws_page.is_displaying_data_for_watering_station(watering_station)
        detail_ws_page.edit_button.click()
        assert update_ws_page.form_has_values_from_watering_station(watering_station)

        # the user then goes back to the garden detail page
        update_ws_page.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(garden_page)

        # the user then clicks the deactivate all button and all watering stations in the table are deactivated
        garden_page.deactivate_button.click()
        for i in range(1, self.num_watering_stations):
            status = garden_page.get_watering_station_field_value(i, 'Status')
            assert not self.ws_status_to_bool(status)

        # the user then clicks the activate all button and all watering statios in the table are activated
        garden_page.activate_button.click()
        for i in range(1, self.num_watering_stations):
            status = garden_page.get_watering_station_field_value(i, 'Status')
            assert self.ws_status_to_bool(status)

        # the user then goes to watering_station page and deletes the watering station
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(detail_ws_page)
        detail_ws_page.edit_button.click()
        self.wait_for_page_to_be_loaded(update_ws_page)
        self.perform_delete_modal_checks(update_ws_page)

        # They are then redirected back to the garden detail page, where they see 1 less watering station
        self.wait_for_page_to_be_loaded(garden_page)
        assert garden_page.get_number_watering_stations() == self.num_watering_stations - 1

    def assert_watering_station_table_contains_correct_headers(self, garden_page):
        assert garden_page.get_number_watering_stations() == self.garden.watering_stations.count()
        assert garden_page.field_is_in_watering_station_table('#')
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

    def ws_status_to_bool(self, status):
        return True if status == WateringStationFormatter.ACTIVE_STATUS_STR else False
