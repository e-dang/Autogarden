from datetime import timedelta
import random

import pytest
from garden.models import (_default_is_connected,
                           _default_moisture_threshold,
                           _default_num_missed_updates, _default_status,
                           _default_update_interval,
                           _default_watering_duration, Garden)
from garden.utils import derive_duration_string
from rest_framework import status
from rest_framework.reverse import reverse

from .base import Base
from .pages.garden_detail_page import GardenDetailPage
from .pages.garden_update_page import GardenUpdatePage
from .pages.watering_station_detail_page import WateringStationDetailPage


@pytest.mark.functional
class TestAPICommunication(Base):
    @pytest.fixture(autouse=True)
    def garden(self, garden_factory, use_tmp_static_dir):
        self.num_watering_stations = 16
        self.garden = garden_factory(watering_stations=self.num_watering_stations,
                                     watering_stations__defaults=True,
                                     is_connected=_default_is_connected(),
                                     last_connection_ip=None,
                                     last_connection_time=None,
                                     update_interval=_default_update_interval(),
                                     num_missed_updates=_default_num_missed_updates())

    @pytest.fixture(autouse=True)
    def url(self, live_server):
        self.url = live_server.url + reverse('garden-detail', kwargs={'pk': self.garden.pk})

    @pytest.mark.django_db
    def test_microcontroller_interaction_with_server(self, api_client):
        # the microcontroller sends a GET request to retrieve the watering station configs from the server
        watering_station_url = reverse('api-watering-stations', kwargs={'pk': self.garden.pk})
        resp = api_client.get(watering_station_url)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data) == self.num_watering_stations
        for ws_config in resp.data:
            assert ws_config['status'] == _default_status()
            assert ws_config['moisture_threshold'] == _default_moisture_threshold()
            assert ws_config['watering_duration'] == _default_watering_duration().total_seconds()

        # immediately after the MC sends a GET request to retrieve the garden update interval duration
        garden_url = reverse('api-garden', kwargs={'pk': self.garden.pk})
        resp = api_client.get(garden_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['update_interval'] == self.garden.update_interval.total_seconds()

        # the MC then performs its operations and POSTs the data from its watering station sensors to the server
        data = []
        for i in range(self.num_watering_stations):
            data.append({
                'moisture_level': random.uniform(0, 100)
            })
        resp = api_client.post(watering_station_url, data=data, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        for record, station in zip(data, self.garden.watering_stations.all()):
            station.records.get(moisture_level=record['moisture_level'])  # should not raise

        # the MC also posts data to the garden api to update its data
        garden_data = {
            'water_level': Garden.LOW
        }
        resp = api_client.patch(garden_url, data=garden_data)
        self.garden.refresh_from_db()
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.garden.water_level == garden_data['water_level']

        # sometime later a user changes the garden conifigs
        self.driver.get(self.url)
        detail_gpage = GardenDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(detail_gpage)
        detail_gpage.edit_button.click()
        update_gpage = GardenUpdatePage(self.driver)
        self.wait_for_page_to_be_loaded(update_gpage)
        update_interval = timedelta(minutes=7, seconds=20)
        update_gpage.garden_update_interval = derive_duration_string(update_interval)
        update_gpage.submit_button.click()
        update_gpage.garden_detail_nav_button.click()
        self.wait_for_page_to_be_loaded(detail_gpage)

        # the user also changes the configs for a watering station
        selected_watering_station = 1
        detail_gpage.watering_station = selected_watering_station
        ws_page = WateringStationDetailPage(self.driver)
        self.wait_for_page_to_be_loaded(ws_page)
        ws_status = not list(self.garden.watering_stations.all())[selected_watering_station].status
        moisture_threshold = 80
        watering_duration = timedelta(minutes=3, seconds=2)
        ws_page.status = ws_status
        ws_page.moisture_threshold = moisture_threshold
        ws_page.watering_duration = derive_duration_string(watering_duration)
        ws_page.submit_button.click()

        # when the MC sends another GET request to the watering station api, it recieves the new updated configs
        resp = api_client.get(watering_station_url)
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
        garden_url = reverse('api-garden', kwargs={'pk': self.garden.pk})
        resp = api_client.get(garden_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['update_interval'] == update_interval.total_seconds()