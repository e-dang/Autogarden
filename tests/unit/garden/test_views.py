
from unittest.mock import Mock, create_autospec, patch

import pytest
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from tests.assertions import assert_render_context_called_with

from garden.views import (GardenDetailView, GardenListView, GardenUpdateView,
                          WateringStationListView, WateringStationUpdateView)

User = get_user_model()


@pytest.fixture
def mock_auth_user():
    return create_autospec(User, is_authenticated=True)


@pytest.mark.unit
class TestGardenListView:
    @patch('garden.views.render')
    def test_GET_only_renders_requesting_users_gardens_in_template(self, mock_render, mock_auth_user):
        request = HttpRequest()
        request.user = mock_auth_user

        resp = GardenListView().get(request)

        assert_render_context_called_with(mock_render, {'gardens': mock_auth_user.gardens.all.return_value})
        assert resp == mock_render.return_value


@pytest.mark.unit
class TestGardenDetailView:
    @patch('garden.views.render')
    def test_GET_passes_garden_as_context_to_render(self, mock_render, mock_auth_user):
        pk = 0
        request = HttpRequest()
        request.user = mock_auth_user

        GardenDetailView().get(request, pk)

        assert_render_context_called_with(mock_render, {'garden': mock_auth_user.gardens.get.return_value})


@pytest.mark.unit
class TestGardenUpdateView:
    @patch('garden.views.render')
    @patch('garden.views.UpdateGardenForm')
    def test_GET_passes_update_garden_form_to_context_of_render(self, mock_form, mock_render, mock_auth_user):
        pk = 1
        request = HttpRequest()
        request.user = mock_auth_user

        GardenUpdateView().get(request, pk)

        assert_render_context_called_with(mock_render, {'form': mock_form.return_value})


@pytest.mark.unit
class TestWateringStationUpdateView:
    @patch('garden.views.render')
    @patch('garden.views.WateringStationForm', autospec=True)
    def test_GET_passes_update_watering_station_form_to_context(self, mock_form_class, mock_render, mock_auth_user):
        garden_pk = 1
        ws_pk = 2
        mock_form = mock_form_class.return_value
        request = HttpRequest()
        request.user = mock_auth_user

        WateringStationUpdateView().get(request, garden_pk, ws_pk)

        assert_render_context_called_with(mock_render, {'form': mock_form})


@pytest.mark.unit
class TestWateringStationListView:
    def test_dispatch_calls_patch_when_method_field_on_request_is_patch(self):
        view = WateringStationListView()
        view.patch = Mock()
        request = HttpRequest()
        request.POST['_method'] = 'patch'

        view.dispatch(request)

        view.patch.assert_called_once_with(request)
