import random
from datetime import timedelta
from time import sleep
import pytest
from garden.models import (Garden,
                           _default_moisture_threshold,
                           _default_status,
                           _default_watering_duration)
from garden.utils import derive_duration_string
from rest_framework import status
from rest_framework.reverse import reverse

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.garden_update_page import GardenUpdatePage
from .pages.watering_station_detail_page import WateringStationDetailPage
from .pages.watering_station_update_page import WateringStationUpdatePage
from tests.assertions import assert_garden_connection_fields_are_updated, assert_model_fields_have_values


@pytest.mark.functional
class TestAPICommunication(Base):
    @pytest.fixture(autouse=True)
    def setup(self, user_factory, garden_factory, live_server, test_password, api_client, token_uuid, use_tmp_static_dir):
        self.email = 'email@demo.com'
        self.user = user_factory(email=self.email, password=test_password)
        self.num_watering_stations = 16
        self.update_frequency = 1
        self.garden = garden_factory(owner=self.user,
                                     watering_stations=self.num_watering_stations,
                                     watering_stations__defaults=True,
                                     is_connected=False,
                                     last_connection_ip=None,
                                     last_connection_time=None,
                                     update_frequency=timedelta(seconds=self.update_frequency),
                                     token__uuid=token_uuid
                                     )
        self.api_client = api_client
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_uuid)
        self.url = live_server.url + reverse('garden-detail', kwargs={'pk': self.garden.pk})
        self.create_authenticated_session(self.user, live_server)

    @pytest.mark.django_db
    def test_microcontroller_interaction_with_server(self):
        # the microcontroller PATCHs data to the garden api to update the garden instance
        garden_data = {
            'water_level': Garden.LOW,
            'connection_strength': random.randint(-100, 0)
        }
        self.send_patch_request_to_garden_api(self.garden, garden_data)

        # afterwards a user visits the garden detail page where they see that the garden info has updated
        self.driver.get(self.url)
        detail_gpage = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_gpage)
        self.garden.refresh_from_db()
        assert detail_gpage.is_displaying_info_for_garden(self.garden)

        # the MC sends a GET request to retrieve the watering station configs from the server
        self.send_get_request_to_watering_station_api(self.garden)

        # immediately after the MC sends a GET request to retrieve the garden update interval duration
        self.send_get_request_to_garden_api(self.garden)

        # the MC then performs its operations and POSTs the data from its watering station sensors to the server
        data = []
        for i in range(self.num_watering_stations):
            data.append({
                'moisture_level': random.uniform(0, 100)
            })
        self.send_post_request_to_watering_station_api(self.garden, data)

        # the microcontroller then crashes and misses an update. The user refreshes the page and sees the updated
        # connection info, where the connection status is not disconnected
        sleep(self.update_frequency)
        self.driver.get(self.url)
        self.wait_for_page_to_be_loaded(detail_gpage)
        self.garden.refresh_from_db()
        assert detail_gpage.is_displaying_info_for_garden(self.garden)
        assert self.garden.is_connected == False

        # the user then change the garden configs
        detail_gpage.edit_button.click()
        update_gpage = GardenUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_gpage)
        update_frequency = timedelta(minutes=7, seconds=20)
        update_gpage.update_garden(update_frequency=derive_duration_string(update_frequency))
        update_gpage.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(detail_gpage)

        # the user also changes the configs for a watering station
        selected_watering_station = 1
        detail_gpage.watering_station = selected_watering_station
        detail_ws_page = WateringStationDetailPage(self.driver)
        detail_ws_page.edit_button.click()
        update_ws_page = WateringStationUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_ws_page)
        ws_status = not list(self.garden.watering_stations.all())[selected_watering_station].status
        moisture_threshold = 80
        watering_duration = timedelta(minutes=3, seconds=2)
        update_ws_page.status = ws_status
        update_ws_page.moisture_threshold = moisture_threshold
        update_ws_page.watering_duration = derive_duration_string(watering_duration)
        update_ws_page.submit_button.click()

        # when the MC sends another GET request to the watering station api, it recieves the new updated configs
        # self.send_get_request_to_watering_station_api(self.garden)
        resp = self.api_client.get(self.get_watering_station_api_url(self.garden))
        assert resp.status_code == status.HTTP_200_OK
        for i, ws_config in enumerate(resp.data, start=1):
            if i == selected_watering_station:
                assert ws_config['status'] == ws_status
                assert ws_config['moisture_threshold'] == moisture_threshold
                assert ws_config['watering_duration'] == watering_duration.total_seconds()
            else:
                assert ws_config['status'] == _default_status()
                assert ws_config['moisture_threshold'] == _default_moisture_threshold()
                assert ws_config['watering_duration'] == _default_watering_duration().total_seconds()

        # similarly when it sends a GET request to the garden api, it recieves the new updated configs
        resp = self.api_client.get(self.get_garden_api_url(self.garden))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['update_frequency'] == update_frequency.total_seconds()

    def get_garden_api_url(self, garden):
        return reverse('api-garden', kwargs={'name': garden.name})

    def get_watering_station_api_url(self, garden):
        return reverse('api-watering-stations', kwargs={'name': garden.name})

    def send_patch_request_to_garden_api(self, garden, data):
        garden_url = self.get_garden_api_url(garden)

        resp = self.api_client.patch(garden_url, data=data)

        garden.refresh_from_db()
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert_model_fields_have_values(data, garden)
        assert_garden_connection_fields_are_updated(garden, resp)

    def send_get_request_to_garden_api(self, garden):
        garden_url = self.get_garden_api_url(garden)

        resp = self.api_client.get(garden_url)

        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['update_frequency'] == self.garden.update_frequency.total_seconds()

        return resp.data

    def send_get_request_to_watering_station_api(self, garden):
        watering_station_url = self.get_watering_station_api_url(garden)

        resp = self.api_client.get(watering_station_url)

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data) == garden.watering_stations.all().count()
        for ws_config in resp.data:
            assert ws_config['status'] == _default_status()
            assert ws_config['moisture_threshold'] == _default_moisture_threshold()
            assert ws_config['watering_duration'] == _default_watering_duration().total_seconds()

        return resp.data

    def send_post_request_to_watering_station_api(self, garden, data):
        watering_station_url = self.get_watering_station_api_url(garden)

        resp = self.api_client.post(watering_station_url, data=data, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        for record, station in zip(data, self.garden.watering_stations.all()):
            station.records.get(moisture_level=record['moisture_level'])  # should not raise
