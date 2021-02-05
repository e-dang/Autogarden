import uuid

import pytest
from django.db.utils import IntegrityError
from microcontroller.models import MicroController
from microcontroller.serializers import MicroControllerSerializer
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED


@pytest.fixture
def data_POST_api_create_micro_controller():
    num_watering_stations = 4
    url = reverse('api-create-micro-controller')
    data = {
        'uuid': uuid.uuid4(),
        'num_watering_stations': num_watering_stations
    }

    return num_watering_stations, url, data


@pytest.mark.integration
class TestViews:
    def test_api_create_micro_controller_view_has_correct_url(self):
        assert reverse('api-create-micro-controller') == '/api/micro-controller/'

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

        assert resp.status_code == HTTP_201_CREATED
        assert resp.data['pk'] == MicroController.objects.get(uuid=data['uuid']).pk


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
class TestMicroControllerManager:
    @pytest.mark.django_db
    def test_create_adds_num_watering_stations_to_micro_controller_instance(self):
        num_watering_stations = 16

        micro_controller = MicroController.objects.create(
            uuid=uuid.uuid4(), num_watering_stations=num_watering_stations)

        assert micro_controller.watering_stations.count() == num_watering_stations


@pytest.mark.integration
class TestMicroControllerSerializer:
    @pytest.mark.django_db
    def test_serializer_requires_num_watering_stations(self):
        serializer = MicroControllerSerializer(data={'uuid': uuid.uuid4()})

        assert serializer.is_valid() is False
        assert serializer.errors['num_watering_stations'][0].code == 'required'
