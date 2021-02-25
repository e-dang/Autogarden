from garden.utils import build_duration_string, derive_duration_string
import pytest
from django.urls import reverse

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.watering_station_detail_page import WateringStationDetailPage
from garden.models import Garden, _default_moisture_threshold, _default_watering_duration


class TestGardenSetup(Base):
    @pytest.fixture(autouse=True)
    def garden(self, garden_factory):
        self.garden = garden_factory(watering_stations=10)

    @pytest.fixture(autouse=True)
    def url(self, live_server):
        self.url = live_server.url + reverse('garden-detail', kwargs={'pk': self.garden.pk})

    def assert_watering_station_has_default_values(self, page):
        assert page.moisture_threshold == str(_default_moisture_threshold())
        assert page.watering_duration == derive_duration_string(_default_watering_duration())
        assert page.plant_type == ''

    @pytest.mark.django_db
    def test_user_can_modify_a_garden(self):
        # a user goes to a garden detail page
        self.driver.get(self.url)
        garden_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(garden_page)

        # they see a table, where each row corresponds to a watering station in the garden and the header of the table
        # displays the field names of the watering_stations
        assert garden_page.get_number_watering_stations() == self.garden.watering_stations.count()
        assert garden_page.field_is_in_watering_station_table('Watering Station Number')
        assert garden_page.field_is_in_watering_station_table('Plant Type')
        assert garden_page.field_is_in_watering_station_table('Moisture Threshold')
        assert garden_page.field_is_in_watering_station_table('Watering Duration')

        # the user also notices that the row display some information about the watering station
        selected_watering_station = 1
        assert str(selected_watering_station) == garden_page.get_watering_station_field_value(
            selected_watering_station, 'Watering Station Number')
        plant_type = garden_page.get_watering_station_field_value(selected_watering_station, 'Plant Type')
        moisture_threshold = garden_page.get_watering_station_field_value(
            selected_watering_station, 'Moisture Threshold')
        watering_duration = garden_page.get_watering_station_field_value(
            selected_watering_station, 'Watering Duration')

        # they click a watering station link and are taken to a page with a form that allows them
        # to edit the configurations of the watering station. The user notices that the values in the form are the same
        # as in the table on the previous page
        garden_page.watering_station = selected_watering_station
        ws_page = WateringStationDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(ws_page)
        assert ws_page.plant_type == plant_type
        assert ws_page.watering_duration == watering_duration
        assert ws_page.moisture_threshold == moisture_threshold
        self.assert_watering_station_has_default_values(ws_page)

        # the user then changes these values and submits the form
        moisture_threshold = '80'
        watering_duration = build_duration_string(minutes=10, seconds=2)
        plant_type = 'lettuce'
        ws_page.moisture_threshold = moisture_threshold
        ws_page.watering_duration = watering_duration
        ws_page.plant_type = plant_type
        ws_page.submit_watering_station_update()

        # they then go back to the garden detail view and select a different watering station page.
        ws_page.go_back_to_garden_detail()
        self.wait_for_page_to_be_loaded(garden_page)
        garden_page.watering_station = selected_watering_station + 1
        self.wait_for_page_to_be_loaded(ws_page)
        self.assert_watering_station_has_default_values(ws_page)

        # they then use the navbar to go directly to the watering station page that they had edited and see that their
        # configurations have persisted
        ws_page.go_to_watering_station_page(selected_watering_station)
        assert ws_page.moisture_threshold == moisture_threshold
        assert ws_page.watering_duration == watering_duration
        assert ws_page.plant_type == plant_type
