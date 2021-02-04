import uuid

import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.functional
class TestMicroControllerInitialization:
    @pytest.mark.django_db
    def test_micro_controller_can_setup_hard_configs_and_get_soft_configs(self, api_client):
        num_watering_stations = 16

        # the micro controller sends a POST request to initialize its hard configs on the server
        hard_configs = {
            'id': uuid.uuid4(),
            'watering_stations': num_watering_stations
        }

        resp = api_client.post(reverse('api-create-micro-controller'), data=hard_configs)
        assert resp.status_code == status.HTTP_201_CREATED

        # the MC then sends a GET request to retrieve the soft configs from the server
        resp = api_client.get(reverse('api-configs'))
        assert resp.status_code == status.HTTP_200_OK
        soft_configs = resp.data

        assert False, 'Finish the test'

        # sometime later a user changes the soft configs and when the MC sends another GET request to the server
        # the MC recieves the new updated soft configs

        # the MC unexpectedly crashes which causes it to be logged. It sends the same login credentials, POST, and GET
        # requests as before and recieves the same updated soft configs