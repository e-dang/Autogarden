
from unittest.mock import Mock, create_autospec, patch

import pytest
from django.http.request import HttpRequest
from rest_framework.request import Request
from tests.assertions import assert_data_contains_fields

from garden import models
from garden.serializers import (GardenGetSerializer, GardenPatchSerializer,
                                WateringStationSerializer)


@pytest.mark.unit
class TestGardenGetSerializer:
    def test_serialized_data_contains_expected_fields(self, garden_factory):
        expected_fields = ['update_frequency']
        garden = garden_factory.build()

        serializer = GardenGetSerializer(garden)

        assert_data_contains_fields(serializer.data, expected_fields)

    def test_get_update_frequency_returns_return_value_of_total_seconds_method_call(self):
        mock_garden = Mock()

        ret_val = GardenGetSerializer().get_update_frequency(mock_garden)

        assert ret_val == mock_garden.update_frequency.total_seconds.return_value


@pytest.mark.unit
class TestGardenPatchSerializer:
    def test_serialized_data_contains_expected_fields(self, garden_factory):
        expected_fields = ['water_level', 'connection_strength']
        garden = garden_factory.build()

        serializer = GardenPatchSerializer(garden)

        assert_data_contains_fields(serializer.data, expected_fields)

    @patch('garden.serializers.serializers.ModelSerializer.save')
    def test_save_calls_update_on_garden_with_request(self, mock_super):
        mock_garden = create_autospec(models.Garden)
        request = Request(HttpRequest())
        serializer = GardenPatchSerializer(instance=mock_garden)

        serializer.save(request)

        mock_garden.update.assert_called_once_with(request)


@pytest.mark.unit
class TestWateringStationSerializer:
    def test_serialized_data_contains_expected_fields(self, watering_station_factory):
        expected_fields = ['moisture_threshold', 'watering_duration', 'status']
        watering_station = watering_station_factory.build()

        serializer = WateringStationSerializer(watering_station)

        assert_data_contains_fields(serializer.data, expected_fields)

    def test_get_watering_duration_returns_return_value_of_total_seconds_method_call(self):
        mock_watering_station = Mock()

        ret_val = WateringStationSerializer().get_watering_duration(mock_watering_station)

        assert ret_val == mock_watering_station.watering_duration.total_seconds.return_value
