import uuid

import pytest
from django.db.utils import IntegrityError
from microcontroller.models import MicroController
from rest_framework.reverse import reverse


@pytest.mark.integration
class TestViews:
    def test_api_create_micro_controller_view_has_correct_url(self):
        assert reverse('api-create-micro-controller') == '/api/micro-controller/'


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
