import pytest
from django.urls import reverse
from garden.utils import build_duration_string
from tests.functional.pages.garden_detail_page import GardenDetailPage

from .base import Base


class TestWateringStationCreation(Base):
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
    def test_user_can_create_watering_station(self):
        # a logged in user is at the garden detail page
        self.driver.get(self.url)
        detail_gpage = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_gpage)

        # they click the add watering station button and see a modal to appear
        detail_gpage.add_watering_station_button.click()
        self.wait_for_modal_to_be_visible(detail_gpage.modal_id)

        # the user then enters invalid information for the new watering station
        moisture_threshold = -1
        watering_duration = -1
        detail_gpage.create_watering_station(moisture_threshold=moisture_threshold, watering_duration=watering_duration)

        # however the user sees errors appear in the form from the invalid inputs
        self.wait_for_form_error('error_1_id_moisture_threshold')
        self.wait_for_form_error('error_1_id_watering_duration')

        # the user then exits out to check if the watering station was added anyway, but finds no extra watering
        # stations in the table
        detail_gpage.cancel_button.click()
        self.wait_for_model_to_disappear(detail_gpage.modal_id)
        assert detail_gpage.get_number_watering_stations() == self.num_watering_stations

        # they then click the add watering station button again and try to add valid information.
        detail_gpage.add_watering_station_button.click()
        self.wait_for_modal_to_be_visible(detail_gpage.modal_id)
        moisture_threshold = 1
        watering_duration = build_duration_string(minutes=4, seconds=32)
        plant_type = 'spinach'
        image = 'test_lettuce_image.png'
        detail_gpage.enter_form_fields(
            plant_type=plant_type,
            moisture_threshold=moisture_threshold,
            watering_duration=watering_duration,
            image=image
        )
        self.perform_image_crop(detail_gpage, image)
        detail_gpage.submit_button.click()

        # this time it works and the user sees another watering station in the table
        self.wait_for_model_to_disappear(detail_gpage.modal_id)
        assert detail_gpage.get_number_watering_stations() == self.num_watering_stations + 1
