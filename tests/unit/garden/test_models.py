from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
import pytz

from garden import models


@pytest.mark.unit
class TestGardenModel:
    @pytest.mark.parametrize('field, get_default', [
        ('name', models._default_garden_name),
        ('is_connected', models._default_is_connected),
        ('update_frequency', models._default_update_frequency),
        ('image', models._default_garden_image)
    ],
        ids=['name', 'is_connected', 'update_frequency', 'image'])
    def test_field_is_given_a_default_value(self, field, get_default):
        garden = models.Garden()

        assert getattr(garden, field) == get_default()

    @pytest.mark.parametrize('garden_factory, is_connected, expected', [
        (None, True, models.Garden.CONNECTED_STR),
        (None, False, models.Garden.DISCONNECTED_STR),
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
        update_frequency = timedelta(minutes=minutes)
        expected = last_connection_time + update_frequency - datetime.now(pytz.UTC)
        garden = garden_factory.build(last_connection_time=last_connection_time, update_frequency=update_frequency)

        ret_val = garden.calc_time_till_next_update()

        assert int(expected.total_seconds()) == ret_val

    def test_calc_time_till_next_update_returns_none_if_prev_connection_has_never_been_established(self, garden_factory):
        update_frequency = timedelta(minutes=5)
        garden = garden_factory.build(last_connection_time=None, update_frequency=update_frequency)

        ret_val = garden.calc_time_till_next_update()

        assert ret_val is None

    def test_calc_time_till_next_update_returns_time_based_on_prev_expected_update_even_if_update_was_missed(self, garden_factory):
        num_updates_missed = 2
        update_frequency_minutes = 5
        last_connection_time = datetime.now(pytz.UTC) - timedelta(minutes=update_frequency_minutes * num_updates_missed)
        update_frequency = timedelta(minutes=update_frequency_minutes)
        expected = last_connection_time + (num_updates_missed + 1) * update_frequency - datetime.now(pytz.UTC)
        garden = garden_factory.build(last_connection_time=last_connection_time, update_frequency=update_frequency)

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

    @pytest.mark.parametrize('value, message', [
        (None, models.Garden.CONN_NOT_AVAILABLE_MSG),
        (-81, models.Garden.CONN_BAD_MSG),
        (-80, models.Garden.CONN_POOR_MSG),
        (-71, models.Garden.CONN_POOR_MSG),
        (-70, models.Garden.CONN_OK_MSG),
        (-68, models.Garden.CONN_OK_MSG),
        (-67, models.Garden.CONN_GOOD_MSG),
        (-31, models.Garden.CONN_GOOD_MSG),
        (-30, models.Garden.CONN_EXCELLENT_MSG),
    ],
        ids=['n/a', 'bad', 'poor_low', 'poor_high', 'ok_low', 'ok_high', 'good_low', 'good_high', 'excellent'])
    def test_get_connection_strength_display_returns_correct_message(self, garden_factory, value, message):
        garden = garden_factory.build(connection_strength=value)

        ret_val = garden.get_connection_strength_display()

        assert ret_val == message

    @pytest.mark.parametrize('update_frequency, expected', [
        (timedelta(minutes=1, seconds=30), '1 Min 30 Sec'),
        (timedelta(minutes=0, seconds=45), '45 Sec'),
        (timedelta(minutes=10), '10 Min')
    ],
        ids=['1:30', '0:45', '10:00'])
    def test_update_frequency_display_returns_correct_string(self, garden_factory, update_frequency, expected):
        garden = garden_factory.build(update_frequency=update_frequency)

        ret_val = garden.update_frequency_display()

        assert ret_val == expected

    @pytest.mark.parametrize('value, klass', [
        (None, models.Garden.CONN_NOT_AVAILABLE_BADGE),
        (-81, models.Garden.CONN_BAD_BADGE),
        (-80, models.Garden.CONN_POOR_BADGE),
        (-71, models.Garden.CONN_POOR_BADGE),
        (-70, models.Garden.CONN_OK_BADGE),
        (-68, models.Garden.CONN_OK_BADGE),
        (-67, models.Garden.CONN_GOOD_BADGE),
        (-31, models.Garden.CONN_GOOD_BADGE),
        (-30, models.Garden.CONN_EXCELLENT_BADGE),
    ],
        ids=['n/a', 'bad', 'poor_low', 'poor_high', 'ok_low', 'ok_high', 'good_low', 'good_high', 'excellent'])
    def test_get_connection_strength_badge_class_returns_correct_class(self, garden_factory, value, klass):
        garden = garden_factory.build(connection_strength=value)

        ret_val = garden.get_connection_strength_badge_class()

        assert ret_val == klass

    @pytest.mark.parametrize('value, klass', [
        (models.Garden.LOW, models.Garden.WL_LOW_BADGE),
        (models.Garden.OK, models.Garden.WL_OK_BADGE)
    ],
        ids=['low', 'ok'])
    def test_get_water_level_badge_class_returns_correct_badge(self, garden_factory, value, klass):
        garden = garden_factory.build(water_level=value)

        ret_val = garden.get_water_level_badge_class()

        assert ret_val == klass

    @pytest.mark.parametrize('value, klass', [
        (True, models.Garden.CONNECTED_BADGE),
        (False, models.Garden.DISCONNECTED_BADGE)
    ],
        ids=['connected', 'disconnected'])
    def test_get_is_connected_badge_class_returns_correct_class(self, garden_factory, value, klass):
        garden = garden_factory.build(is_connected=value)

        ret_val = garden.get_is_connected_badge_class()

        assert ret_val == klass


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
