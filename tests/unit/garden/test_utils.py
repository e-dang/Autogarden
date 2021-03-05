from datetime import timedelta
from unittest.mock import create_autospec, patch

import pytest

import garden.utils as utils
from garden import models


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
