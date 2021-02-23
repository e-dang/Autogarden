import uuid
from datetime import timedelta
import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from garden.models import Garden


@pytest.mark.functional
class TestGardenInitialization:
    @pytest.mark.django_db
    def test_garden_can_setup_hard_configs_and_get_soft_configs(self, api_client):
        num_watering_stations = 16

        # the microcontroller sends a POST request to initialize its configs on the server
        garden_configs = {
            'uuid': uuid.uuid4(),
            'num_watering_stations': num_watering_stations
        }

        init_url = reverse('api-garden')
        resp = api_client.post(init_url, data=garden_configs)
        assert resp.status_code == status.HTTP_201_CREATED
        pk = int(resp.data['pk'])  # should not raise

        # the MC then sends a GET request to retrieve the watering station configs from the server
        watering_station_url = reverse('api-watering-stations', kwargs={'pk': pk})
        resp = api_client.get(watering_station_url)
        assert resp.status_code == status.HTTP_200_OK
        for i in range(num_watering_stations):
            assert 'moisture_threshold' in resp.data[i]
            assert 'watering_duration' in resp.data[i]

        watering_station_data = resp.data

        # sometime later a user changes the watering station and when the MC sends another GET request to the server
        # the MC recieves the new updated watering station configs
        mt_diff = 1
        wd_diff = timedelta(minutes=1)
        garden = Garden.objects.get(pk=pk)
        for watering_station in garden.watering_stations.all():
            watering_station.moisture_threshold += mt_diff
            watering_station.watering_duration += wd_diff
            watering_station.save()

        resp = api_client.get(watering_station_url)
        assert resp.status_code == status.HTTP_200_OK
        for i in range(num_watering_stations):
            assert resp.data[i]['moisture_threshold'] == watering_station_data[i]['moisture_threshold'] + mt_diff
            assert resp.data[i]['watering_duration'] == self.add_time_delta(
                watering_station_data[i]['watering_duration'], wd_diff)

        watering_station_data = resp.data

        # the MC unexpectedly crashes which causes it to repeat the same operations as before. This time it does not
        # recieve a HTTP_201_CREATED status code, but recieves the same pk.
        resp = api_client.post(init_url, data=garden_configs)
        assert resp.status_code == status.HTTP_409_CONFLICT
        assert pk == int(resp.data['pk'])

        # it then makes a request for the watering station configs and recieves the same updated watering station
        # configs as before
        resp = api_client.get(watering_station_url)
        assert resp.status_code == status.HTTP_200_OK
        for i in range(num_watering_stations):
            assert resp.data[i] == watering_station_data[i]

    def add_time_delta(self, duration, increment):
        hours, minutes, seconds = duration.split(':')
        duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        duration = duration + increment
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)
