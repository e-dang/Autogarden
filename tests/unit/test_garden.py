import pytest
from garden.models import (Garden, WateringStation,
                           _default_moisture_threshold,
                           _default_watering_duration, _default_garden_name)
from garden.serializers import (NEGATIVE_NUM_WATERING_STATIONS_ERR,
                                GardenSerializer, WateringStationSerializer)
from rest_framework.serializers import ValidationError


@pytest.mark.unit
class TestGardenSerializer:
    @pytest.mark.parametrize('garden_factory, field', [
        (None, 'uuid'),
    ],
        indirect=['garden_factory'],
        ids=['uuid'])
    def test_field_is_serialized(self, garden_factory, field):
        garden = garden_factory.build()

        serializer = GardenSerializer(garden)

        assert field in serializer.data

    def test_validate_num_watering_stations_raises_validation_error_when_value_is_negative(self):
        value = -1
        serializer = GardenSerializer()

        with pytest.raises(ValidationError) as err:
            serializer.validate_num_watering_stations(value)
            assert str(err) == NEGATIVE_NUM_WATERING_STATIONS_ERR


@pytest.mark.unit
class TestGardenModel:
    @pytest.mark.parametrize('field, get_default', [
        ('name', _default_garden_name),
    ],
        ids=['name'])
    def test_field_is_given_a_default_value(self, field, get_default):
        garden = Garden()

        assert getattr(garden, field) == get_default()


@pytest.mark.unit
class TestWateringStationModel:
    @pytest.mark.parametrize('field, get_default', [
        ('moisture_threshold', _default_moisture_threshold),
        ('watering_duration', _default_watering_duration)
    ],
        ids=['moisture_threshold', 'watering_duration'])
    def test_field_is_given_a_default_value(self, field, get_default):
        watering_station = WateringStation(garden=Garden())

        assert getattr(watering_station, field) == get_default()


@pytest.mark.unit
class TestWateringStationSerializer:
    @pytest.mark.parametrize('watering_station_factory, field', [
        (None, 'moisture_threshold'),
        (None, 'watering_duration'),
    ],
        indirect=['watering_station_factory'],
        ids=['moisture_threshold', 'watering_duration'])
    def test_field_is_serialized(self, watering_station_factory, field):
        watering_station = watering_station_factory.build()

        serializer = WateringStationSerializer(watering_station)

        assert field in serializer.data
