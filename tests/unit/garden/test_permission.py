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
