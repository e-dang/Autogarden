import pytest
from django.urls import reverse
from garden.models import _default_garden_name

from .base import Base, wait_for
from .pages.garden_list_page import GardenListPage
from .pages.garden_detail_page import GardenDetailPage


class TestGardenSetup(Base):
    @pytest.fixture(autouse=True)
    def url(self, live_server):
        return live_server.url + reverse('garden-list')

    @pytest.mark.django_db
    def test_user_can_create_a_garden(self, url):
        # a user goes to the garden page
        self.driver.get(url)
        list_page = GardenListPage(self.driver)
        self.wait_for_page_to_be_loaded(list_page)

        # they see a list of registered gardens which is currently 0
        assert list_page.get_number_of_gardens() == 0

        # they also see an option to create a new garden, which they click and immediately see a modal that prompts
        # them for the garden name. The default garden name is displayed in that text box. They are also prompted for
        # the number of watering stations that are going to be in this garden
        list_page.click_add_new_garden()
        assert list_page.new_garden_name == _default_garden_name()
        assert list_page.num_watering_stations == ''

        # they enter a negative number for the number of watering stations and hit enter, and they see a error message
        # appear
        list_page.num_watering_stations = -1
        list_page.submit_new_garden()
        wait_for(lambda: self.driver.find_element_by_id('error_1_id_num_watering_stations'))

        # now they enter a garden name and valid number of watering stations and see a new garden appear in the list of
        # gardens
        garden_name = 'My New Garden'
        num_watering_stations = 3
        list_page.new_garden_name = garden_name
        list_page.num_watering_stations = num_watering_stations
        list_page.submit_new_garden()
        list_page.wait_for_garden_in_list(garden_name)

        # they click on the garden and are taken to the associated garden page
        list_page.click_garden(garden_name)
        detail_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_page)

        # they see the watering stations that are part of the garden
        assert detail_page.get_number_watering_stations() == num_watering_stations
