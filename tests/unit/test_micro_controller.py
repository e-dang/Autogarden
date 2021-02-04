import pytest

from rest_framework.serializers import ValidationError
from microcontroller.serializers import MicroControllerSerializer, NEGATIVE_NUM_WATERING_STATIONS_ERR


@pytest.mark.unit
class TestMicroControllerSerializer:
    def test_validate_num_watering_stations_raises_validation_error_when_value_is_negative(self):
        value = -1
        serializer = MicroControllerSerializer()

        with pytest.raises(ValidationError) as err:
            serializer.validate_num_watering_stations(value)
            assert str(err) == NEGATIVE_NUM_WATERING_STATIONS_ERR
