from datetime import datetime, timedelta
from garden.forms import NewGardenForm, WateringStationForm
from garden.permissions import TokenPermission
from pathlib import Path
from typing import Dict
from unittest.mock import Mock, create_autospec, patch
from django.forms import ValidationError

import garden.utils as utils
import pytest
import pytz
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from garden import models
from garden.serializers import GardenGetSerializer, WateringStationSerializer
from garden.views import (GardenDetailView, GardenListView, GardenUpdateView,
                          WateringStationListView, WateringStationUpdateView)

User = get_user_model()


@pytest.fixture
def mock_auth_user():
    return create_autospec(User, is_authenticated=True)


def assert_render_context_called_with(mock_render: Mock, kwarg: Dict) -> None:
    for key, item in kwarg.items():
        assert mock_render.call_args.kwargs['context'][key] == item


@pytest.mark.unit
class TestGardenSerializer:
    @pytest.mark.parametrize('garden_factory, field', [
        (None, 'update_interval'),
    ],
        indirect=['garden_factory'],
        ids=['uuid'])
    def test_field_is_serialized(self, garden_factory, field):
        garden = garden_factory.build()

        serializer = GardenGetSerializer(garden)

        assert field in serializer.data

    def test_get_update_interval_returns_return_value_of_total_seconds_method_call(self):
        mock_garden = Mock()

        ret_val = GardenGetSerializer().get_update_interval(mock_garden)

        assert ret_val == mock_garden.update_interval.total_seconds.return_value


@pytest.mark.unit
class TestGardenModel:
    @pytest.mark.parametrize('field, get_default', [
        ('name', models._default_garden_name),
        ('is_connected', models._default_is_connected),
        ('update_interval', models._default_update_interval),
        ('num_missed_updates', models._default_num_missed_updates),
        ('image', models._default_garden_image)
    ],
        ids=['name', 'is_connected', 'update_interval', 'num_missed_updates', 'image'])
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

    def test_calc_time_till_next_update_returns_expected_time_to_within_a_second(self, garden_factory):
        minutes = 10
        last_connection_time = datetime.now(pytz.UTC) - timedelta(minutes=minutes - 2)
        update_interval = timedelta(minutes=minutes)
        expected = last_connection_time + update_interval - datetime.now(pytz.UTC)
        garden = garden_factory.build(last_connection_time=last_connection_time, update_interval=update_interval)

        ret_val = garden.calc_time_till_next_update()

        assert int(expected.total_seconds()) == ret_val

    def test_calc_time_till_next_update_returns_none_if_prev_connection_has_never_been_established(self, garden_factory):
        update_interval = timedelta(minutes=5)
        garden = garden_factory.build(last_connection_time=None, update_interval=update_interval)

        ret_val = garden.calc_time_till_next_update()

        assert ret_val is None

    def test_calc_time_till_next_update_returns_time_based_on_prev_expected_update_even_if_update_was_missed(self, garden_factory):
        num_updates_missed = 2
        update_interval_minutes = 5
        last_connection_time = datetime.now(pytz.UTC) - timedelta(minutes=update_interval_minutes * num_updates_missed)
        update_interval = timedelta(minutes=update_interval_minutes)
        expected = last_connection_time + (num_updates_missed + 1) * update_interval - datetime.now(pytz.UTC)
        garden = garden_factory.build(last_connection_time=last_connection_time, update_interval=update_interval)

        ret_val = garden.calc_time_till_next_update()

        assert int(expected.total_seconds()) == ret_val

    def test_get_formatted_last_connection_time_returns_correct_format(self, garden_factory):
        day = 25
        month = 2
        year = 2021
        hour = 12
        minute = 13
        period = 'PM'
        dtime = datetime(day=day, month=month, year=year, hour=hour, minute=minute, tzinfo=pytz.UTC)
        garden = garden_factory.build(last_connection_time=dtime)

        ret_val = garden.get_formatted_last_connection_time()

        assert ret_val == f'{month}/{day}/{year} {hour}:{minute} {period}'

    def test_get_formatted_last_connection_time_returns_None_if_last_connection_time_is_none(self, garden_factory):
        garden = garden_factory.build(last_connection_time=None)

        ret_val = garden.get_formatted_last_connection_time()

        assert ret_val == str(None)

    @patch('garden.models.settings')
    def test_get_abs_path_to_image_returns_full_path_to_image_file(self, mock_settings, garden_factory):
        garden = garden_factory.build()
        str_path = '/test/root/'
        mock_settings.STATIC_ROOT = Path(str_path)

        path = garden.get_abs_path_to_image()

        assert str(path) == str_path + f'images/{models._default_garden_image()}'


@pytest.mark.unit
class TestWateringStationModel:
    @pytest.mark.parametrize('field, get_default', [
        ('moisture_threshold', models._default_moisture_threshold),
        ('watering_duration', models._default_watering_duration),
        ('status', models._default_status)
    ],
        ids=['moisture_threshold', 'watering_duration', 'status'])
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

    @pytest.mark.parametrize('watering_station_factory, status, expected', [
        (None, True, models.WateringStation.ACTIVE_STATUS_STR),
        (None, False, models.WateringStation.INACTIVE_STATUS_STR),
    ],
        indirect=['watering_station_factory'],
        ids=['active', 'inactive'])
    def test_status_string_returns_correct_string_based_on_status(self, watering_station_factory, status, expected):
        station = watering_station_factory.build(status=status)

        ret_val = station.status_string

        assert ret_val == expected


@pytest.mark.unit
class TestWateringStationSerializer:
    @pytest.mark.parametrize('watering_station_factory, field', [
        (None, 'moisture_threshold'),
        (None, 'watering_duration'),
        (None, 'status')
    ],
        indirect=['watering_station_factory'],
        ids=['moisture_threshold', 'watering_duration', 'status'])
    def test_field_is_serialized(self, watering_station_factory, field):
        watering_station = watering_station_factory.build()

        serializer = WateringStationSerializer(watering_station)

        assert field in serializer.data

    def test_get_watering_duration_returns_return_value_of_total_seconds_method_call(self):
        mock_watering_station = Mock()

        ret_val = WateringStationSerializer().get_watering_duration(mock_watering_station)

        assert ret_val == mock_watering_station.watering_duration.total_seconds.return_value


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
class TestGardenListView:
    @patch('garden.views.render')
    def test_GET_only_renders_requesting_users_gardens_in_template(self, mock_render, mock_auth_user):
        request = HttpRequest()
        request.user = mock_auth_user

        resp = GardenListView().get(request)

        assert_render_context_called_with(mock_render, {'gardens': mock_auth_user.gardens.all.return_value})
        assert resp == mock_render.return_value


@pytest.mark.unit
class TestGardenDetailView:
    @patch('garden.views.render')
    def test_GET_passes_garden_as_context_to_render(self, mock_render, mock_auth_user):
        pk = 0
        request = HttpRequest()
        request.user = mock_auth_user

        GardenDetailView().get(request, pk)

        assert_render_context_called_with(mock_render, {'garden': mock_auth_user.gardens.get.return_value})


@pytest.mark.unit
class TestGardenUpdateView:
    @patch('garden.views.render')
    @patch('garden.views.UpdateGardenForm')
    def test_GET_passes_update_garden_form_to_context_of_render(self, mock_form, mock_render, mock_auth_user):
        pk = 1
        request = HttpRequest()
        request.user = mock_auth_user

        GardenUpdateView().get(request, pk)

        assert_render_context_called_with(mock_render, {'form': mock_form.return_value})


@pytest.mark.unit
class TestWateringStationUpdateView:
    @patch('garden.views.render')
    @patch('garden.views.WateringStationForm', autospec=True)
    def test_GET_passes_update_watering_station_form_to_context(self, mock_form_class, mock_render, mock_auth_user):
        garden_pk = 1
        ws_pk = 2
        mock_form = mock_form_class.return_value
        request = HttpRequest()
        request.user = mock_auth_user

        WateringStationUpdateView().get(request, garden_pk, ws_pk)

        assert_render_context_called_with(mock_render, {'form': mock_form})


@pytest.mark.unit
class TestWateringStationListView:
    def test_dispatch_calls_patch_when_method_field_on_request_is_patch(self):
        view = WateringStationListView()
        view.patch = Mock()
        request = HttpRequest()
        request.POST['_method'] = 'patch'

        view.dispatch(request)

        view.patch.assert_called_once_with(request)


@pytest.mark.unit
class TestTokenPermission:
    def test_has_object_permission_returns_false_when_no_auth_headers_are_set(self, garden_factory):
        mock_view = Mock()
        garden = garden_factory.build()
        request = HttpRequest()

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == False

    def test_has_object_permission_returns_false_when_auth_header_token_is_different_than_garden_token(self, garden_factory):
        mock_view = Mock()
        garden = garden_factory.build()
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + str(garden.token.uuid) + 'extra_chars'

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == False

    def test_has_object_permission_returns_true_when_auth_header_token_matches_garden_token(self, garden_factory):
        mock_view = Mock()
        garden = garden_factory.build()
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + str(garden.token.uuid)

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == True
