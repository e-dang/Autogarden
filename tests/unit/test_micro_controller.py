import pytest
from microcontroller.models import (MicroController, WateringStation,
                                    _default_moisture_threshold,
                                    _default_watering_duration)
from microcontroller.serializers import (NEGATIVE_NUM_WATERING_STATIONS_ERR,
                                         MicroControllerSerializer, WateringStationSerializer)
from rest_framework.serializers import ValidationError


@pytest.mark.unit
class TestMicroControllerSerializer:
    @pytest.mark.parametrize('micro_controller_factory, field', [
        (None, 'uuid'),
    ],
        indirect=['micro_controller_factory'],
        ids=['uuid'])
    def test_field_is_serialized(self, micro_controller_factory, field):
        micro_controller = micro_controller_factory.build()

        serializer = MicroControllerSerializer(micro_controller)

        assert field in serializer.data

    def test_validate_num_watering_stations_raises_validation_error_when_value_is_negative(self):
        value = -1
        serializer = MicroControllerSerializer()

        with pytest.raises(ValidationError) as err:
            serializer.validate_num_watering_stations(value)
            assert str(err) == NEGATIVE_NUM_WATERING_STATIONS_ERR


@pytest.mark.unit
class TestWateringStationModel:
    @pytest.mark.parametrize('field, get_default', [
        ('moisture_threshold', _default_moisture_threshold),
        ('watering_duration', _default_watering_duration)
    ],
        ids=['moisture_threshold', 'watering_duration'])
    def test_field_is_given_a_default_value(self, field, get_default):
        watering_station = WateringStation(micro_controller=MicroController())

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
