from datetime import timedelta, datetime
from garden.models import Garden
from unittest.mock import Mock, patch

import pytest
import pytz

from garden.formatters import GardenFormatter, ModelFormatter, WateringStationFormatter, format_duration


@pytest.mark.parametrize('duration, expected', [
    (timedelta(minutes=1, seconds=30), '1 Min 30 Sec'),
    (timedelta(minutes=0, seconds=45), '45 Sec'),
    (timedelta(minutes=10), '10 Min')
],
    ids=['1:30', '0:45', '10:00'])
def test_format_duration(duration, expected):
    ret_val = format_duration(duration.total_seconds())

    assert ret_val == expected


@pytest.mark.unit
class TestModelFormatter:
    def test_attribute_on_model_formatter_is_retrieved_if_it_exists(self):
        attr = 'test_attribute'
        mock_instance = Mock()
        mock_method = Mock()
        formatter = ModelFormatter(mock_instance)
        setattr(formatter, attr, mock_method)

        ret_val = getattr(formatter, attr)

        assert ret_val is mock_method

    def test_function_that_has_pattern_get_name_display_is_called_when_accessed_through_name(self):
        attr = 'test_attribute'
        mock_instance = Mock()
        mock_method = Mock()
        formatter = ModelFormatter(mock_instance)
        setattr(formatter, f'get_{attr}_display', mock_method)

        ret_val = getattr(formatter, attr)

        mock_method.assert_called_once()
        assert ret_val == mock_method.return_value

    def test_attribute_on_formatter_instance_variable_is_called_if_formatter_doesnt_have_same_named_attr_or_overriden_get_method(self):
        attr = 'test_attribute'
        mock_instance = Mock()
        mock_method = Mock()
        setattr(mock_instance, f'{attr}', mock_method)
        formatter = ModelFormatter(mock_instance)

        ret_val = getattr(formatter, attr)

        assert ret_val is mock_method


@pytest.mark.unit
class TestGardenFormatter:
    @pytest.mark.parametrize('garden_factory, is_connected, expected', [
        (None, True, GardenFormatter.CONNECTED_STR),
        (None, False, GardenFormatter.DISCONNECTED_STR),
    ],
        indirect=['garden_factory'],
        ids=['connected', 'disconnected'])
    def test_get_is_connected_display_returns_correct_string(self, garden_factory, is_connected, expected):
        formatter = GardenFormatter(garden_factory.build(is_connected=is_connected))

        ret_val = formatter.get_is_connected_display()

        assert ret_val == expected

    @pytest.mark.parametrize('value, klass', [
        (True, GardenFormatter.CONNECTED_BADGE),
        (False, GardenFormatter.DISCONNECTED_BADGE)
    ],
        ids=['connected', 'disconnected'])
    def test_get_is_connected_badge_class_returns_correct_class(self, garden_factory, value, klass):
        formatter = GardenFormatter(garden_factory.build(is_connected=value))

        ret_val = formatter.get_is_connected_badge_class()

        assert ret_val == klass

    def test_get_is_connected_element_return_value_contains_is_connected_display_and_badge_classes(self, garden_factory):
        formatter = GardenFormatter(garden_factory.build())
        ret1 = 'ret1'
        ret2 = 'ret2'
        formatter.get_is_connected_display = Mock(return_value=ret1)
        formatter.get_is_connected_badge_class = Mock(return_value=ret2)

        ret_val = formatter.get_is_connected_element()

        assert formatter.get_is_connected_display.return_value in ret_val
        assert formatter.get_is_connected_badge_class.return_value in ret_val

    @pytest.mark.parametrize('value, message', [
        (None, GardenFormatter.CONN_NOT_AVAILABLE_MSG),
        (-81, GardenFormatter.CONN_BAD_MSG),
        (-80, GardenFormatter.CONN_POOR_MSG),
        (-71, GardenFormatter.CONN_POOR_MSG),
        (-70, GardenFormatter.CONN_OK_MSG),
        (-68, GardenFormatter.CONN_OK_MSG),
        (-67, GardenFormatter.CONN_GOOD_MSG),
        (-31, GardenFormatter.CONN_GOOD_MSG),
        (-30, GardenFormatter.CONN_EXCELLENT_MSG),
    ],
        ids=['n/a', 'bad', 'poor_low', 'poor_high', 'ok_low', 'ok_high', 'good_low', 'good_high', 'excellent'])
    def test_get_connection_strength_display_returns_correct_message(self, garden_factory, value, message):
        formatter = GardenFormatter(garden_factory.build(connection_strength=value))

        ret_val = formatter.get_connection_strength_display()

        assert ret_val == message

    @pytest.mark.parametrize('value, klass', [
        (None, GardenFormatter.CONN_NOT_AVAILABLE_BADGE),
        (-81, GardenFormatter.CONN_BAD_BADGE),
        (-80, GardenFormatter.CONN_POOR_BADGE),
        (-71, GardenFormatter.CONN_POOR_BADGE),
        (-70, GardenFormatter.CONN_OK_BADGE),
        (-68, GardenFormatter.CONN_OK_BADGE),
        (-67, GardenFormatter.CONN_GOOD_BADGE),
        (-31, GardenFormatter.CONN_GOOD_BADGE),
        (-30, GardenFormatter.CONN_EXCELLENT_BADGE),
    ],
        ids=['n/a', 'bad', 'poor_low', 'poor_high', 'ok_low', 'ok_high', 'good_low', 'good_high', 'excellent'])
    def test_get_connection_strength_badge_class_returns_correct_class(self, garden_factory, value, klass):
        formatter = GardenFormatter(garden_factory.build(connection_strength=value))

        ret_val = formatter.get_connection_strength_badge_class()

        assert ret_val == klass

    def test_get_connection_strength_element_return_value_contains_connection_strength_display_and_badge_classes(self, garden_factory):
        formatter = GardenFormatter(garden_factory.build())
        ret1 = 'ret1'
        ret2 = 'ret2'
        formatter.get_connection_strength_display = Mock(return_value=ret1)
        formatter.get_connection_strength_badge_class = Mock(return_value=ret2)

        ret_val = formatter.get_connection_strength_element()

        assert formatter.get_connection_strength_display.return_value in ret_val
        assert formatter.get_connection_strength_badge_class.return_value in ret_val

    @pytest.mark.parametrize('value, klass', [
        (Garden.LOW, GardenFormatter.WL_LOW_BADGE),
        (Garden.OK, GardenFormatter.WL_OK_BADGE)
    ],
        ids=['low', 'ok'])
    def test_get_water_level_badge_class_returns_correct_badge(self, garden_factory, value, klass):
        formatter = GardenFormatter(garden_factory.build(water_level=value))

        ret_val = formatter.get_water_level_badge_class()

        assert ret_val == klass

    def test_get_water_level_element_return_value_contains_water_level_display_and_badge_classes(self, garden_factory):
        formatter = GardenFormatter(garden_factory.build())
        ret1 = 'ret1'
        formatter.get_water_level_badge_class = Mock(return_value=ret1)

        ret_val = formatter.get_water_level_element()

        assert formatter.instance.get_water_level_display() in ret_val
        assert formatter.get_water_level_badge_class.return_value in ret_val

    @patch('garden.formatters.format_duration')
    def test_get_update_frequency_display_calls_format_duration_and_returns_its_return_value(self, mock_format_duration, garden_factory):
        garden = garden_factory.build(update_frequency=timedelta(minutes=1))
        formatter = GardenFormatter(garden)

        ret_val = formatter.get_update_frequency_display()

        mock_format_duration.assert_called_once_with(garden.update_frequency.total_seconds())
        assert ret_val == mock_format_duration.return_value

    def test_get_last_connection_time_display_returns_correct_format(self, garden_factory):
        day = 25
        month = 2
        year = 2021
        hour = 12
        minute = 13
        period = 'PM'
        dtime = datetime(day=day, month=month, year=year, hour=hour, minute=minute, tzinfo=pytz.UTC)
        formatter = GardenFormatter(garden_factory.build(last_connection_time=dtime))

        ret_val = formatter.get_last_connection_time_display()

        assert ret_val == f'{month}/{day}/{year} {hour}:{minute} {period}'

    def test_get_last_connection_time_display_returns_none_if_last_connection_time_is_none(self, garden_factory):
        formatter = GardenFormatter(garden_factory.build(last_connection_time=None))

        ret_val = formatter.get_last_connection_time_display()

        assert ret_val == str(None)


@pytest.mark.unit
class TestWateringStationFormatter:
    @patch('garden.formatters.format_duration')
    def test_get_watering_duration_display_calls_format_duration_and_returns_its_return_value(self, mock_format_duration, watering_station_factory):
        watering_station = watering_station_factory.build(watering_duration=timedelta(minutes=1))
        formatter = WateringStationFormatter(watering_station)

        ret_val = formatter.get_watering_duration_display()

        mock_format_duration.assert_called_once_with(watering_station.watering_duration.total_seconds())
        assert ret_val == mock_format_duration.return_value

    @pytest.mark.parametrize('status, expected', [
        (True, WateringStationFormatter.ACTIVE_STATUS_STR),
        (False, WateringStationFormatter.INACTIVE_STATUS_STR),
    ],
        ids=['active', 'inactive'])
    def test_get_status_display_returns_correct_string(self, watering_station_factory, status, expected):
        formatter = WateringStationFormatter(watering_station_factory.build(status=status))

        ret_val = formatter.get_status_display()

        assert ret_val == expected

    @pytest.mark.parametrize('status, expected', [
        (True, WateringStationFormatter.ACTIVE_STATUS_BADGE),
        (False, WateringStationFormatter.INACTIVE_STATUS_BADGE)
    ],
        ids=['active', 'inactive'])
    def test_get_status_badge_class_returns_the_correct_class(self, watering_station_factory, status, expected):
        formatter = WateringStationFormatter(watering_station_factory.build(status=status))

        ret_val = formatter.get_status_badge_class()

        assert ret_val == expected

    def test_get_status_element_return_value_contains_status_display_and_badge_classes(self, watering_station_factory):
        formatter = WateringStationFormatter(watering_station_factory.build())
        ret1 = 'ret1'
        ret2 = 'ret2'
        formatter.get_status_display = Mock(return_value=ret1)
        formatter.get_status_badge_class = Mock(return_value=ret2)

        ret_val = formatter.get_status_element()

        assert formatter.get_status_display.return_value in ret_val
        assert formatter.get_status_badge_class.return_value in ret_val
