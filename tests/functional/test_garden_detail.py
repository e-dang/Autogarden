from datetime import timedelta
from garden.forms import duration_string
import pytest
from django.urls import reverse

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
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
        assert page.watering_duration == duration_string(_default_watering_duration())

    @pytest.mark.django_db
    def test_user_can_create_a_garden(self):
        # a user goes to a garden detail page
        self.driver.get(self.url)
        page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(page)

        # they see a row of buttons, where each corresponds to a watering station in the garden
        assert page.get_number_watering_stations() == self.garden.watering_stations.count()

        # they click a watering station button and see a form appear under the button row taht allows them
        # to edit the configurations of the watering station
        selected_watering_station = 1
        page.watering_station = selected_watering_station
        self.assert_watering_station_has_default_values(page)

        # the user then changes these values and submits the form
        moisture_threshold = 80
        watering_duration = duration_string(timedelta(minutes=10, seconds=2))
        page.moisture_threshold = moisture_threshold
        page.watering_duration = watering_duration
        page.submit_watering_station_update()

        # they then click to another watering station and then back again and see that the changes have persisted
        page.watering_station = selected_watering_station + 1
        self.assert_watering_station_has_default_values(page)
        page.watering_station = selected_watering_station
        assert page.moisture_threshold == moisture_threshold
        assert page.watering_duration == watering_duration

        assert False, 'Finish the test'
