from unittest.mock import Mock

import pytest
from django.http.request import HttpRequest

from garden.permissions import TokenPermission
from garden.models import Token


@pytest.mark.integration
class TestTokenPermission:
    @pytest.fixture(autouse=True)
    def garden(self, garden_factory):
        garden = garden_factory()
        garden.token.delete()
        return garden

    @pytest.fixture(autouse=True)
    def uuid(self):
        return 'random_chars'

    @pytest.fixture(autouse=True)
    def token(self, garden, uuid):
        Token.objects.create(garden=garden, uuid=uuid)

    @pytest.mark.django_db
    def test_has_object_permission_returns_false_when_auth_header_token_is_different_than_garden_token(self, garden, uuid):
        mock_view = Mock()
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = f'Token {uuid}_extra_chars'

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == False

    @pytest.mark.django_db
    def test_has_object_permission_returns_true_when_auth_header_token_matches_garden_token(self, garden, uuid):
        mock_view = Mock()
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = f'Token {uuid}'

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == True
