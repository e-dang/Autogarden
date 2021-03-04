from garden.models import Garden
import re
import pytest

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.garden_list_page import GardenListPage
from django.urls import reverse
from rest_framework import status


class TestDataAccessability(Base):
    @pytest.fixture(autouse=True)
    def setup(self, live_server, test_password, use_tmp_static_dir):
        self.live_server = live_server
        self.url = self.create_url(reverse('garden-list'))
        self.email = 'email@demo.com'
        self.create_pre_authenticated_session(self.email, test_password, live_server)

    @pytest.mark.django_db
    def test_users_can_only_access_the_data_that_they_own(self, test_password, api_client):
        # an authenticated user goes to the website and adds a garden to their page
        self.driver.get(self.url)
        list_gpage = GardenListPage(self.driver)
        self.wait_for_page_to_be_loaded(list_gpage)
        assert list_gpage.get_number_of_gardens() == 0

        garden_name = 'My New Garden'
        num_watering_stations = 3
        garden_image = 'test_garden_image.png'
        update_interval = '0:10:00'
        list_gpage.add_garden(garden_name, num_watering_stations, garden_image, update_interval)
        list_gpage.wait_for_garden_in_list(garden_name)

        # they go to the newly created garden detail page and notice that it has a unique url
        list_gpage.click_garden(garden_name)
        detail_page = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_page)
        detail_url = self.driver.current_url

        # they then logout
        detail_page.logout_button.click()

        # later another user logs in and sees their garden list page, which is empty
        new_email = 'random_person@demo.com'
        self.create_pre_authenticated_session(new_email, test_password, self.live_server)
        self.driver.get(self.url)
        self.wait_for_page_to_be_loaded(list_gpage)
        assert list_gpage.get_number_of_gardens() == 0

        # they somehow know that the previous user had made a garden and could access it at a unique url, so they
        # manually enter that url into the browser. They see a 404 error appear instead of the garden
        # detail page
        self.driver.get(detail_url)
        self.assert_404_error()

        # the user then tries all urls associated with that garden to try and gain access to it, but fails
        res = re.search(r'/(\d+)/', detail_url)
        pk = res.groups()[0]
        garden = Garden.objects.get(pk=pk)
        watering_station = garden.watering_stations.first()

        self.driver.get(self.create_url(garden.get_update_url()))
        self.assert_404_error()

        self.driver.get(self.create_url(garden.get_delete_url()))
        self.assert_404_error()

        self.driver.get(self.create_url(watering_station.get_absolute_url()))
        self.assert_404_error()

        self.driver.get(self.create_url(watering_station.get_update_url()))
        self.assert_404_error()

        self.driver.get(self.create_url(watering_station.get_delete_url()))
        self.assert_404_error()

        # the user then tries to use the api to view and modify the other users data, but that doesnt work as well
        resp = api_client.get(self.create_api_url(garden.get_absolute_url()))
        self.assert_403_forbidden(resp)

        resp = api_client.patch(self.create_api_url(garden.get_absolute_url()))
        self.assert_403_forbidden(resp)

        resp = api_client.get(self.create_api_url(garden.get_watering_stations_url()))
        self.assert_403_forbidden(resp)

        resp = api_client.post(self.create_api_url(garden.get_watering_stations_url()))
        self.assert_403_forbidden(resp)

    def assert_404_error(self):
        assert '404 Error. Page Not Found.' in self.driver.find_element_by_tag_name('body').text

    def assert_403_forbidden(self, response):
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'].code == 'not_authenticated'

    def create_url(self, path):
        return self.live_server.url + path

    def create_api_url(self, path):
        return ''.join([self.live_server.url, '/api', path])
