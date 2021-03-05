
from unittest.mock import Mock

import pytest
from django.http.request import HttpRequest

from garden.permissions import TokenPermission


@pytest.mark.unit
class TestTokenPermission:
    def test_has_object_permission_returns_false_when_no_auth_headers_are_set(self, garden_factory):
        mock_view = Mock()
        garden = garden_factory.build()
        request = HttpRequest()

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == False

    def test_has_object_permission_returns_false_when_auth_header_token_is_different_than_garden_token(self, garden_factory):
        mock_view = Mock()
        garden = garden_factory.build()
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + str(garden.token.uuid) + 'extra_chars'

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == False

    def test_has_object_permission_returns_true_when_auth_header_token_matches_garden_token(self, garden_factory):
        mock_view = Mock()
        garden = garden_factory.build()
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + str(garden.token.uuid)

        ret_val = TokenPermission().has_object_permission(request, mock_view, garden)

        assert ret_val == True
