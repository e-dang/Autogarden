import pytest
from tests.assertions import assert_serializer_required_field_error

from garden.serializers import GardenPatchSerializer


@pytest.mark.integration
class TestGardenPatchSerializer:
    @pytest.mark.django_db
    def test_is_valid_returns_false_when_required_field_is_missing(self, garden_missing_patch_serializer_data):
        data, field = garden_missing_patch_serializer_data

        serializer = GardenPatchSerializer(data=data)

        assert serializer.is_valid() == False
        assert_serializer_required_field_error(serializer.errors[field])
