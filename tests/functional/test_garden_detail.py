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
        page.watering_station = 1
        assert page.moisture_threshold == _default_moisture_threshold()
        assert page.watering_duration == _default_watering_duration()

        assert False, 'Finish the test'
