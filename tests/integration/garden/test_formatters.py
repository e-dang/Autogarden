from unittest.mock import patch

import pytest

from garden.formatters import GardenFormatter, WateringStationFormatter


@pytest.mark.integration
class TestGardenFormatter:
    @pytest.mark.django_db
    @patch('garden.formatters.TokenFormatter')
    def test_get_token_display_returns_the_token_creation_date_and_return_value_of_token_formatter(self, mock_token_formatter, garden_factory, token_factory):
        mock_token_formatter.return_value.uuid = 'random stuff'
        garden = garden_factory()
        formatter = GardenFormatter(garden)

        ret_val = formatter.get_token_display()

        assert mock_token_formatter.return_value.uuid in ret_val
        assert str(garden.token) in ret_val


@pytest.mark.integration
class TestWateringStationFormatter:
    @pytest.mark.django_db
    def test_get_idx_display_returns_string_of_number_1_greater_than_actual_idx(self, watering_station):
        formatter = WateringStationFormatter(watering_station)

        ret_val = formatter.get_idx_display()

        assert ret_val == '1'

    @pytest.mark.django_db
    def test_get_name_display_returns_name_that_contains_the_idx_display_of_the_watering_station(self, watering_station):
        formatter = WateringStationFormatter(watering_station)

        ret_val = formatter.get_name_display()

        assert '#1' in ret_val
