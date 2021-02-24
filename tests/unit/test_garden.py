from unittest.mock import create_autospec, patch

import garden.utils as utils
import pytest
from django.http.request import HttpRequest
from garden.models import (Garden, WateringStation, _default_garden_name,
                           _default_moisture_threshold,
                           _default_watering_duration)
from garden.serializers import (NEGATIVE_NUM_WATERING_STATIONS_ERR,
                                GardenSerializer, WateringStationSerializer)
from garden.views import GardenDetailView
from rest_framework.serializers import ValidationError


@pytest.mark.unit
class TestGardenSerializer:
    @pytest.mark.parametrize('garden_factory, field', [
        (None, 'uuid'),
    ],
        indirect=['garden_factory'],
        ids=['uuid'])
    def test_field_is_serialized(self, garden_factory, field):
        garden = garden_factory.build()

        serializer = GardenSerializer(garden)

        assert field in serializer.data

    def test_validate_num_watering_stations_raises_validation_error_when_value_is_negative(self):
        value = -1
        serializer = GardenSerializer()

        with pytest.raises(ValidationError) as err:
            serializer.validate_num_watering_stations(value)
            assert str(err) == NEGATIVE_NUM_WATERING_STATIONS_ERR


@pytest.mark.unit
class TestGardenModel:
    @pytest.mark.parametrize('field, get_default', [
        ('name', _default_garden_name),
    ],
        ids=['name'])
    def test_field_is_given_a_default_value(self, field, get_default):
        garden = Garden()

        assert getattr(garden, field) == get_default()


@pytest.mark.unit
class TestWateringStationModel:
    @pytest.mark.parametrize('field, get_default', [
        ('moisture_threshold', _default_moisture_threshold),
        ('watering_duration', _default_watering_duration)
    ],
        ids=['moisture_threshold', 'watering_duration'])
    def test_field_is_given_a_default_value(self, field, get_default):
        watering_station = WateringStation(garden=Garden())

        assert getattr(watering_station, field) == get_default()


@pytest.mark.unit
class TestWateringStationSerializer:
    @pytest.mark.parametrize('watering_station_factory, field', [
        (None, 'moisture_threshold'),
        (None, 'watering_duration'),
    ],
        indirect=['watering_station_factory'],
        ids=['moisture_threshold', 'watering_duration'])
    def test_field_is_serialized(self, watering_station_factory, field):
        watering_station = watering_station_factory.build()

        serializer = WateringStationSerializer(watering_station)

        assert field in serializer.data


@pytest.mark.unit
class TestUtils:
    @patch('garden.utils.Garden', autospec=True)
    @patch('garden.utils.uuid4')
    def test_create_unique_uuid_calls_uuid_until_a_unique_one_is_found(self, mock_uuid, mock_garden):
        calls = []
        call_count = 2
        for _ in range(call_count):
            calls.append(True)
        calls.append(False)
        mock_garden.objects.filter.return_value.exists.side_effect = calls

        utils.create_unique_garden_uuid()

        assert mock_uuid.call_count == call_count + 1

    @patch('garden.utils.Garden', autospec=True)
    @patch('garden.utils.uuid4')
    def test_create_unique_uuid_returns_the_last_return_value_of_uuid4(self, mock_uuid, mock_garden):
        ret_val = 'test-uuid'
        mock_uuid.return_value = ret_val
        mock_garden.objects.filter.return_value.exists.return_value = False

        uuid = utils.create_unique_garden_uuid()

        assert uuid == ret_val

    @pytest.mark.parametrize('curr_num, target_num', [
        (0, 4),
        (4, 3),
        (4, 4)
    ],
        ids=['<', '>', '='])
    def test_set_num_watering_stations_calls_create_on_garden_related_manager_until_garden_has_the_specified_num_of_watering_stations(self, curr_num, target_num):
        mock_garden = create_autospec(Garden)
        mock_garden.watering_stations.count.return_value = curr_num
        num_watering_stations = target_num

        utils.set_num_watering_stations(mock_garden, num_watering_stations)

        assert mock_garden.watering_stations.create.call_count == max(0, target_num - curr_num)


@pytest.mark.unit
class TestGardenDetailView:
    @patch('garden.views.render')
    @patch('garden.views.Garden', autospec=True)
    def test_GET_passes_garden_as_context_to_render(self, mock_garden_clas, mock_render):
        mock_garden = mock_garden_clas.objects.get.return_value
        request = HttpRequest()
        pk = 0

        GardenDetailView().get(request, pk)

        assert mock_render.call_args.kwargs['context']['garden'] == mock_garden
