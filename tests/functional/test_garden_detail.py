from garden.utils import build_duration_string, derive_duration_string
import pytest
from django.urls import reverse

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.watering_station_detail_page import WateringStationDetailPage
from garden.models import _default_moisture_threshold, _default_watering_duration


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

    @pytest.mark.django_db
    def test_user_can_modify_a_garden(self):
        # a user goes to a garden detail page
        self.driver.get(self.url)
        garden_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(garden_page)

        # they see a list, where each row corresponds to a watering station in the garden
        assert garden_page.get_number_watering_stations() == self.garden.watering_stations.count()

        # they click a watering station link and are taken to a page with a form that allows them
        # to edit the configurations of the watering station
        selected_watering_station = 1
        garden_page.watering_station = selected_watering_station
        ws_page = WateringStationDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(ws_page)
        self.assert_watering_station_has_default_values(ws_page)

        # the user then changes these values and submits the form
        moisture_threshold = '80'
        watering_duration = build_duration_string(minutes=10, seconds=2)
        ws_page.moisture_threshold = moisture_threshold
        ws_page.watering_duration = watering_duration
        ws_page.submit_watering_station_update()

        # # they then click to another watering station and then back again and see that the changes have persisted
        # page.watering_station = selected_watering_station + 1
        # self.assert_watering_station_has_default_values(page)
        # page.watering_station = selected_watering_station
        # assert page.moisture_threshold == moisture_threshold
        # assert page.watering_duration == watering_duration
