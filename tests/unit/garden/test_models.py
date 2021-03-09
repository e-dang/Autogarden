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
