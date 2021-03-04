from garden.utils import derive_duration_string
import pytest
from django.urls import reverse
from garden.models import _default_garden_name, _default_update_interval
from tests.conftest import assert_image_files_equal

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.garden_list_page import GardenListPage


class TestGardenSetup(Base):
    @pytest.fixture(autouse=True)
    def create_url(self, live_server, test_password, use_tmp_static_dir):
        self.live_server = live_server
        self.url = live_server.url + reverse('garden-list')
        self.email = 'email@demo.com'
        self.create_pre_authenticated_session(self.email, test_password, live_server)

    @pytest.mark.django_db
    def test_user_can_create_a_garden(self):
        # a user goes to the garden page
        self.driver.get(self.url)
        list_page = GardenListPage(self.driver)
        self.wait_for_page_to_be_loaded(list_page)

        # they see a list of registered gardens which is currently 0
        assert list_page.get_number_of_gardens() == 0

        # they also see an option to create a new garden, which they click and immediately see a modal that prompts
        # them for the garden name. The default garden name is displayed in that text box. They are also prompted for
        # the number of watering stations that are going to be in this garden, an image, and the update interval
        list_page.new_garden_button.click()
        self.wait_for_modal_to_be_visible(list_page.modal_id)
        assert list_page.new_garden_name == _default_garden_name()
        assert list_page.num_watering_stations == ''
        assert list_page.update_interval == str(derive_duration_string(_default_update_interval()))
        assert list_page.garden_image

        # they cancel out of the modal, but then re-enter again
        list_page.cancel_button.click()
        self.wait_for_model_to_disappear(list_page.modal_id)
        list_page.new_garden_button.click()
        self.wait_for_modal_to_be_visible(list_page.modal_id)

        # they enter a negative number for the number of watering stations and hit enter, and they see a error message
        # appear
        list_page.num_watering_stations = -1
        list_page.update_interval = -1
        list_page.submit_button.click()
        self.wait_for_form_error('error_1_id_num_watering_stations')
        self.wait_for_form_error('error_1_id_update_interval')

        # now they enter a garden name and valid number of watering stations and see a new garden appear in the list of
        # gardens
        garden_name = 'My New Garden'
        num_watering_stations = 3
        garden_image = 'test_garden_image.png'
        update_interval = '0:10:00'
        list_page.new_garden_name = garden_name
        list_page.num_watering_stations = num_watering_stations
        list_page.update_interval = update_interval
        self.perform_image_crop(list_page, garden_image)
        list_page.submit_button.click()
        list_page.wait_for_garden_in_list(garden_name)
        assert_image_files_equal(list_page.get_garden_image(garden_name), garden_image)

        # they click on the garden and are taken to the associated garden page
        list_page.click_garden(garden_name)
        detail_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_page)

        # they see the watering stations that are part of the garden
        assert detail_page.get_number_watering_stations() == num_watering_stations

        # the user then clicks the AutoGarden tag in the nav bar to navigate home and is taken back to the garden
        # list page
        list_page.home_button.click()
        self.wait_for_page_to_be_loaded(list_page)
