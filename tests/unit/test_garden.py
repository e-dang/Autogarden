from datetime import timedelta
from unittest.mock import Mock, create_autospec, patch

import garden.utils as utils
import pytest
from django.http.request import HttpRequest
# from garden.models import (Garden, WateringStation, _default_garden_name,
#                            _default_moisture_threshold,
#                            _default_watering_duration, _default_is_connected)
from garden import models
from garden.serializers import (NEGATIVE_NUM_WATERING_STATIONS_ERR,
                                GardenSerializer, WateringStationSerializer)
from garden.views import GardenDetailView, WateringStationDetailView
from rest_framework.serializers import ValidationError


def assert_render_context_called_with(mock_render, kwarg):
    assert mock_render.call_args.kwargs['context'] == kwarg


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
        ('name', models._default_garden_name),
        ('is_connected', models._default_is_connected)
    ],
        ids=['name', 'is_connected'])
    def test_field_is_given_a_default_value(self, field, get_default):
        garden = models.Garden()

        assert getattr(garden, field) == get_default()

    @pytest.mark.parametrize('garden_factory, is_connected, expected', [
        (None, True, models.CONNECTED_STR),
        (None, False, models.DISCONNECTED_STR),
    ],
        indirect=['garden_factory'],
        ids=['connected', 'disconnected'])
    def test_status_returns_connected_if_is_connected_is_true(self, garden_factory, is_connected, expected):
        garden = garden_factory.build(is_connected=is_connected)

        ret_val = garden.status

        assert ret_val == expected


@pytest.mark.unit
class TestWateringStationModel:
    @pytest.mark.parametrize('field, get_default', [
        ('moisture_threshold', models._default_moisture_threshold),
        ('watering_duration', models._default_watering_duration)
    ],
        ids=['moisture_threshold', 'watering_duration'])
    def test_field_is_given_a_default_value(self, field, get_default):
        watering_station = models.WateringStation(garden=models.Garden())

        assert getattr(watering_station, field) == get_default()

    @patch('garden.models.derive_duration_string')
    def test_get_formatted_duration_calls_derive_duration_string_with_watering_duration_field(self, mock_derive_duration_string):
        mock_ws = Mock()

        models.WateringStation.get_formatted_duration(mock_ws)

        mock_derive_duration_string.assert_called_once_with(mock_ws.watering_duration)

    @patch('garden.models.derive_duration_string')
    def test_get_formatted_duration_returns_return_value_of_derive_duration_string(self, mock_derive_duration_string):
        mock_ws = Mock()

        ret_val = models.WateringStation.get_formatted_duration(mock_ws)

        assert ret_val == mock_derive_duration_string.return_value


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
    @patch('garden.utils.apps.get_model', autospec=True)
    @patch('garden.utils.uuid4')
    def test_create_unique_uuid_calls_uuid_until_a_unique_one_is_found(self, mock_uuid, mock_get_model):
        mock_garden = mock_get_model.return_value
        calls = []
        call_count = 2
        for _ in range(call_count):
            calls.append(True)
        calls.append(False)
        mock_garden.objects.filter.return_value.exists.side_effect = calls

        utils.create_unique_garden_uuid()

        assert mock_uuid.call_count == call_count + 1

    @patch('garden.utils.apps.get_model', autospec=True)
    @patch('garden.utils.uuid4')
    def test_create_unique_uuid_returns_the_last_return_value_of_uuid4(self, mock_uuid, mock_get_model):
        mock_garden = mock_get_model.return_value
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
        mock_garden = create_autospec(models.Garden)
        mock_garden.watering_stations.count.return_value = curr_num
        num_watering_stations = target_num

        utils.set_num_watering_stations(mock_garden, num_watering_stations)

        assert mock_garden.watering_stations.create.call_count == max(0, target_num - curr_num)

    @pytest.mark.parametrize('minutes, seconds', [
        (0, 0),
        (4, 1),
        (10, 20)
    ],
        ids=['zeros', 'single_digits', 'double_digits'])
    def test_derive_duration_string_returns_minutes_seconds_repr_of_timedelta(self, minutes, seconds):
        duration = timedelta(minutes=minutes, seconds=seconds)

        ret_val = utils.derive_duration_string(duration)

        assert ret_val == f'{minutes:02}:{seconds:02}'

    @patch('garden.utils.timedelta')
    @patch('garden.utils.derive_duration_string')
    def test_build_duration_string_calls_derive_duration_string_with_timedelta_built_from_args(self, mock_derive, mock_timedelta):
        minutes = 1
        seconds = 2

        ret_val = utils.build_duration_string(minutes, seconds)

        assert ret_val == mock_derive.return_value
        mock_derive.assert_called_once_with(mock_timedelta.return_value)
        mock_timedelta.assert_called_once_with(minutes=minutes, seconds=seconds)


@pytest.mark.unit
class TestGardenDetailView:
    @patch('garden.views.render')
    @patch('garden.views.Garden', autospec=True)
    def test_GET_passes_garden_as_context_to_render(self, mock_garden_clas, mock_render):
        mock_garden = mock_garden_clas.objects.get.return_value
        request = HttpRequest()
        pk = 0

        GardenDetailView().get(request, pk)

        assert_render_context_called_with(mock_render, {'garden': mock_garden})


@pytest.mark.unit
class TestWateringStationDetailView:
    @patch('garden.views.Garden')
    @patch('garden.views.render')
    @patch('garden.views.UpdateWateringStationForm', autospec=True)
    def test_GET_passes_update_watering_station_form_to_context(self, mock_form_class, mock_render, mock_garden):
        garden_pk = 1
        ws_pk = 2
        mock_form = mock_form_class.return_value
        request = HttpRequest()

        WateringStationDetailView().get(request, garden_pk, ws_pk)

        assert_render_context_called_with(mock_render, {'form': mock_form})
