import pytest
from django.urls import reverse
from garden.models import (_default_moisture_threshold, _default_status,
                           _default_watering_duration)
from garden.utils import build_duration_string, derive_duration_string
from tests.conftest import assert_image_files_equal

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.garden_list_page import GardenListPage
from .pages.garden_update_page import GardenUpdatePage
from .pages.watering_station_detail_page import WateringStationDetailPage
from .pages.watering_station_update_page import WateringStationUpdatePage


class TestGardenModification(Base):
    @pytest.fixture(autouse=True)
    def garden(self, garden_factory, use_tmp_static_dir):
        self.num_watering_stations = 10
        self.garden = garden_factory(watering_stations=self.num_watering_stations, watering_stations__defaults=True)

    @pytest.fixture(autouse=True)
    def url(self, live_server):
        self.url = live_server.url + reverse('garden-detail', kwargs={'pk': self.garden.pk})

    @pytest.mark.django_db
    def test_user_can_modify_a_garden_and_its_watering_stations(self):
        # a user goes to a garden detail page
        self.driver.get(self.url)
        garden_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(garden_page)

        # the user sees information about the garden
        self.assert_garden_info_is_correct(garden_page)

        # they see a table, where each row corresponds to a watering station in the garden and the header of the table
        # displays the field names of the watering_stations
        self.assert_watering_station_table_contains_correct_headers(garden_page)

        # the user also notices that the row display some information about the watering station
        selected_watering_station = 1
        assert str(selected_watering_station) == garden_page.get_watering_station_field_value(
            selected_watering_station, 'Watering Station Number')
        table_data = garden_page.get_water_station_data_from_table(selected_watering_station)

        # they click a watering station link and are taken to the watering station detail page.
        garden_page.watering_station = selected_watering_station
        detail_ws_page = WateringStationDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_ws_page)

        # they see an edit button on the page and click it.
        detail_ws_page.edit_button.click()

        # they are taken to a page with a form that allows them to edit the configurations of the watering station.
        # The user notices that the values in the form are the same as in the previous pages
        update_ws_page = WateringStationUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_ws_page)
        self.assert_watering_station_has_values(table_data, update_ws_page)
        self.assert_watering_station_has_default_values(update_ws_page)

        # the user then changes these values and submits the form
        ws_status = not table_data['status']
        plant_type = 'lettuce'
        moisture_threshold = '80'
        watering_duration = build_duration_string(minutes=10, seconds=2)
        update_ws_page.status = ws_status
        update_ws_page.plant_type = plant_type
        update_ws_page.moisture_threshold = moisture_threshold
        update_ws_page.watering_duration = watering_duration
        update_ws_page.submit_button.click()

        # they then go back to the garden detail view and sees that the changes have been persisted in the table
        update_ws_page.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(garden_page)
        table_data = garden_page.get_water_station_data_from_table(selected_watering_station)
        assert ws_status == table_data['status']
        assert plant_type == table_data['plant_type']
        assert moisture_threshold == table_data['moisture_threshold']
        assert watering_duration == table_data['watering_duration']

        # the user then selects a different watering station page
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(update_ws_page)
        self.assert_watering_station_has_default_values(update_ws_page)

        # they then use the navbar to go directly to the watering station page that they had edited and see that their
        # configurations have persisted
        update_ws_page.go_to_watering_station_page(selected_watering_station)
        self.assert_watering_station_has_values(table_data, update_ws_page)

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
            assert not garden_page.convert_watering_station_status_to_bool(status)

        # the user then goes to watering_station page and deletes the watering station
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(update_ws_page)
        self.perform_delete_modal_checks(update_ws_page)

        # They are then redirected back to the garden detail page, where they see 1 less watering station
        self.wait_for_page_to_be_loaded(garden_page)
        assert garden_page.get_number_watering_stations() == self.num_watering_stations

        # the user then clicks the edit button and is taken to update garden page
        garden_page.edit_button.click()
        update_gpage = GardenUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_gpage)

        # the user sees a form that lets them change the name of the garden, upload a different picture for the garden,
        # and delete the garden. They enter a new name and photo for the garden and submit the form.
        new_garden_name = 'My new garden name'
        new_garden_image = 'test_garden_image.png'
        update_interval = '10:00'
        update_gpage.garden_name = new_garden_name
        update_gpage.garden_update_interval = update_interval
        update_gpage.garden_image = new_garden_image
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
        assert update_gpage.garden_name == new_garden_name
        assert update_gpage.garden_update_interval == update_interval
        assert_image_files_equal(update_gpage.garden_image, new_garden_image)

        # the user then deletes the garden
        self.perform_delete_modal_checks(update_gpage)

        # they are then redirected back to the garden list page where they see no gardens
        list_gpage = GardenListPage(self.driver)
        self.wait_for_page_to_be_loaded(list_gpage)
        assert list_gpage.get_number_of_gardens() == 0

    def assert_watering_station_has_default_values(self, ws_page):
        data = {
            'status': _default_status(),
            'plant_type': '',
            'moisture_threshold': str(_default_moisture_threshold()),
            'watering_duration': derive_duration_string(_default_watering_duration())
        }
        self.assert_watering_station_has_values(data, ws_page)

    def assert_watering_station_has_values(self, data, ws_page):
        for key, value in data.items():
            assert getattr(ws_page, key) == value

    def assert_garden_info_is_correct(self, garden_page):
        assert garden_page.get_garden_status() == self.garden.status
        assert garden_page.get_last_connected_from() == str(self.garden.last_connection_ip)
        assert garden_page.get_last_connected_at() == self.garden.get_formatted_last_connection_time()
        self.assert_next_expected_update_is_correct(garden_page)
        assert garden_page.get_num_missed_updates() == str(self.garden.num_missed_updates)
        assert garden_page.get_water_level() == str(self.garden.get_water_level_display())

    def assert_next_expected_update_is_correct(self, garden_page):
        assert self.garden.calc_time_till_next_update() - int(garden_page.get_next_expected_update()) < 2

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
        page.cancel_delete_button.click()
        self.wait_for_model_to_disappear(page.modal_id)
        page.delete_button.click()
        self.wait_for_modal_to_be_visible(page.modal_id)
        page.confirm_delete_button.click()
