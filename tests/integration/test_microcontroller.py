import uuid

import pytest
from django.db.utils import IntegrityError
from microcontroller.models import MicroController
from microcontroller.serializers import (MicroControllerSerializer,
                                         WateringStationSerializer)
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.fixture
def data_POST_api_create_micro_controller():
    num_watering_stations = 4
    url = reverse('api-create-micro-controller')
    data = {
        'uuid': uuid.uuid4(),
        'num_watering_stations': num_watering_stations
    }

    return num_watering_stations, url, data


@pytest.fixture
def data_GET_api_get_watering_stations(micro_controller_factory):
    num_watering_stations = 4
    micro_controller = micro_controller_factory(watering_stations=num_watering_stations)
    url = reverse('api-get-watering-stations', kwargs={'pk': micro_controller.pk})

    return num_watering_stations, micro_controller, url


@pytest.mark.integration
class TestViews:
    @pytest.mark.parametrize('view, kwargs, expected', [
        ('api-create-micro-controller', {}, '/api/micro-controller/'),
        ('api-get-watering-stations', {'pk': 0}, '/api/micro-controller/0/watering-stations/'),
    ],
        ids=['api-create-micro-controller', 'garden'])
    def test_view_has_correct_url(self, view, kwargs, expected):
        assert reverse(view, kwargs=kwargs) == expected

    @pytest.mark.django_db
    def test_POST_api_create_micro_controller_creates_micro_controller_obj_with_specified_num_watering_stations(self, api_client, data_POST_api_create_micro_controller):
        num_watering_stations, url, data = data_POST_api_create_micro_controller

        api_client.post(url, data=data)

        assert MicroController.objects.count() == 1
        micro_controller = MicroController.objects.get(uuid=data['uuid'])
        assert micro_controller.watering_stations.count() == num_watering_stations

    @pytest.mark.django_db
    def test_POST_api_create_micro_controller_returns_201_response_with_pk_data(self, api_client, data_POST_api_create_micro_controller):
        _, url, data = data_POST_api_create_micro_controller

        resp = api_client.post(url, data=data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data['pk'] == MicroController.objects.get(uuid=data['uuid']).pk

    @pytest.mark.django_db
    def test_POST_api_create_micro_controller_returns_409_response_if_micro_controller_with_uuid_already_exists(self, api_client, micro_controller_factory, data_POST_api_create_micro_controller):
        _, url, data = data_POST_api_create_micro_controller
        micro_controller_factory(uuid=data['uuid'])

        resp = api_client.post(url, data=data)

        assert resp.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.django_db
    def test_POST_api_create_micro_controller_returns_pk_of_micro_controller_if_uuid_already_exists(self, api_client, micro_controller_factory, data_POST_api_create_micro_controller):
        _, url, data = data_POST_api_create_micro_controller
        micro_controller = micro_controller_factory(uuid=data['uuid'])

        resp = api_client.post(url, data=data)

        assert int(resp.data['pk']) == micro_controller.pk

    @pytest.mark.django_db
    def test_GET_api_get_watering_stations_returns_200_response(self, api_client, data_GET_api_get_watering_stations):
        _, _, url = data_GET_api_get_watering_stations

        resp = api_client.get(url)

        assert resp.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_GET_api_get_watering_stations_returns_serialized_watering_station_data_belonging_to_micro_controller(self, api_client, data_GET_api_get_watering_stations):
        num_watering_stations, micro_controller, url = data_GET_api_get_watering_stations

        resp = api_client.get(url)

        assert len(resp.data) == num_watering_stations
        watering_stations = list(micro_controller.watering_stations.all())
        for i, watering_station in enumerate(resp.data):
            assert watering_station == WateringStationSerializer(watering_stations[i]).data


@pytest.mark.integration
class TestMicroControllerModel:
    @pytest.mark.django_db
    def test_uuid_field_must_be_unique(self):
        id_ = uuid.uuid4()
        MicroController(uuid=id_).save()

        with pytest.raises(IntegrityError) as err:
            MicroController(uuid=id_).save()
            assert 'UNIQUE' in err


@pytest.mark.integration
class TestMicroControllerSerializer:
    @pytest.mark.django_db
    def test_serializer_requires_num_watering_stations(self):
        serializer = MicroControllerSerializer(data={'uuid': uuid.uuid4()})

        assert serializer.is_valid() is False
        assert serializer.errors['num_watering_stations'][0].code == 'required'

    @pytest.mark.django_db
    def test_create_adds_num_watering_stations_to_micro_controller_instance(self):
        num_watering_stations = 16
        serializer = MicroControllerSerializer()

        micro_controller = serializer.create({'uuid': uuid.uuid4(), 'num_watering_stations': num_watering_stations})

        assert micro_controller.watering_stations.count() == num_watering_stations
