from garden.utils import build_duration_string, derive_duration_string
import pytest
from django.urls import reverse

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.watering_station_detail_page import WateringStationDetailPage
from garden.models import _default_moisture_threshold, _default_watering_duration, _default_status


class TestGardenSetup(Base):
    @pytest.fixture(autouse=True)
    def garden(self, garden_factory):
        self.garden = garden_factory(watering_stations=10, watering_stations__defaults=True)

    @pytest.fixture(autouse=True)
    def url(self, live_server):
        self.url = live_server.url + reverse('garden-detail', kwargs={'pk': self.garden.pk})

    @pytest.mark.django_db
    def test_user_can_modify_a_garden(self):
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

        # they click a watering station link and are taken to a page with a form that allows them
        # to edit the configurations of the watering station. The user notices that the values in the form are the same
        # as in the table on the previous page
        garden_page.watering_station = selected_watering_station
        ws_page = WateringStationDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(ws_page)
        self.assert_watering_station_has_values(table_data, ws_page)
        self.assert_watering_station_has_default_values(ws_page)

        # the user then changes these values and submits the form
        ws_status = not table_data['status']
        plant_type = 'lettuce'
        moisture_threshold = '80'
        watering_duration = build_duration_string(minutes=10, seconds=2)
        ws_page.status = ws_status
        ws_page.plant_type = plant_type
        ws_page.moisture_threshold = moisture_threshold
        ws_page.watering_duration = watering_duration
        ws_page.submit_button.click()

        # they then go back to the garden detail view and sees that the changes have been persisted in the table
        ws_page.go_back_to_garden_detail()
        self.wait_for_page_to_be_loaded(garden_page)
        table_data = garden_page.get_water_station_data_from_table(selected_watering_station)
        assert ws_status == table_data['status']
        assert plant_type == table_data['plant_type']
        assert moisture_threshold == table_data['moisture_threshold']
        assert watering_duration == table_data['watering_duration']

        # the user then selects a different watering station page
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(ws_page)
        self.assert_watering_station_has_default_values(ws_page)

        # they then use the navbar to go directly to the watering station page that they had edited and see that their
        # configurations have persisted
        ws_page.go_to_watering_station_page(selected_watering_station)
        self.assert_watering_station_has_values(table_data, ws_page)

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
        assert garden_page.get_status() == self.garden.status
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
