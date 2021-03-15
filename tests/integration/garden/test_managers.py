import pytest
from django.contrib.auth.hashers import check_password

from garden.models import Token


@pytest.mark.integration
class TestTokenManager:
    @pytest.fixture(autouse=True)
    def garden(self, garden_factory):
        return garden_factory(token=None)

    @pytest.mark.django_db
    def test_create_saves_token_to_garden_instance(self, garden):
        token = Token.objects.create(garden=garden)

        assert garden.token == token

    @pytest.mark.django_db
    def test_create_saves_uuid_as_random_hash(self, garden):
        uuid = 'random uuid'

        token = Token.objects.create(garden=garden, uuid=uuid)

        assert token.uuid != uuid
        assert check_password(uuid, token.uuid)
