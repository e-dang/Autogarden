import pytest
from tests.assertions import assert_data_contains_fields

from garden.serializers import GardenPatchSerializer


@pytest.mark.integration
class TestGardenPatchSerializer:
    @pytest.mark.django_db
    def test_serialized_data_contains_expected_fields(self, garden_patch_serializer_fields):
        expected_fields = ['water_level', 'connection_strength']

        serializer = GardenPatchSerializer(data=garden_patch_serializer_fields)

        assert serializer.is_valid() == True
        assert_data_contains_fields(serializer.data, expected_fields)
