from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import pytz

from garden import models


@pytest.mark.unit
class TestGardenModel:
    @pytest.mark.parametrize('field, get_default', [
        ('name', models._default_garden_name),
        ('is_connected', models._default_is_connected),
        ('update_interval', models._default_update_interval),
        ('image', models._default_garden_image)
    ],
        ids=['name', 'is_connected', 'update_interval', 'image'])
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

    @pytest.mark.parametrize('value, message', [
        (-81, models.Garden.CONN_BAD_MSG),
        (-80, models.Garden.CONN_POOR_MSG),
        (-71, models.Garden.CONN_POOR_MSG),
        (-70, models.Garden.CONN_OK_MSG),
        (-68, models.Garden.CONN_OK_MSG),
        (-67, models.Garden.CONN_GOOD_MSG),
        (-31, models.Garden.CONN_GOOD_MSG),
        (-30, models.Garden.CONN_EXCELLENT_MSG),
    ],
        ids=['bad', 'poor_low', 'poor_high', 'ok_low', 'ok_high', 'good_low', 'good_high', 'excellent'])
    def test_get_connection_strength_display_returns_correct_message(self, garden_factory, value, message):
        garden = garden_factory.build(connection_strength=value)

        ret_val = garden.get_connection_strength_display()

        assert ret_val == message


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
