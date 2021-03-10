import pytest

from garden.formatters import WateringStationFormatter


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
