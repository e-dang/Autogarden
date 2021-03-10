from datetime import datetime, timedelta

import pytest
import pytz

from garden import models
from garden.formatters import WateringStationFormatter


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

    def test__str__returns_garden_name(self, garden_factory):
        garden = garden_factory.build()

        ret_val = garden.__str__()

        assert garden.name in ret_val


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

    def test___str__returns_garden_name_and_watering_station_idx(self, garden_factory, watering_station_factory):
        watering_station = watering_station_factory.build(garden=garden_factory.build())

        ret_val = watering_station.__str__()

        assert str(watering_station.garden) in ret_val
        assert str(watering_station.idx) in ret_val

    def test_get_formatter_returns_a_watering_station_formatter_initialized_with_self(self, watering_station_factory):
        watering_station = watering_station_factory.build()

        ret_val = watering_station.get_formatter()

        assert isinstance(ret_val, WateringStationFormatter)
        assert ret_val.instance is watering_station


@pytest.mark.unit
class TestTokenModel:
    def test___str___method_returns_str_of_uuid(self, token_factory):
        token = token_factory.build()

        ret_val = token.__str__()

        assert ret_val == str(token.uuid)


@pytest.mark.unit
class TestWateringStationRecord:
    def test__str__method_returns_str_containing_garden_watering_station_date(self, watering_station_record_factory):
        record = watering_station_record_factory.build()

        ret_val = record.__str__()

        assert str(record.watering_station.garden) in ret_val
        assert str(record.watering_station.idx) in ret_val
        assert str(record.created) in ret_val
