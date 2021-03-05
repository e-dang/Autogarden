from datetime import datetime, timedelta
from typing import Any, Dict, Iterable
from unittest.mock import Mock

import pytz
from django import http
from garden.models import Garden
from rest_framework import status


def assert_image_files_equal(image_path1: str, image_path2: str) -> None:
    assert image_path1.split('/')[-1] == image_path2.split('/')[-1]


def assert_template_is_rendered(response: http.HttpResponse, template_name: str, expected_status: int = status.HTTP_200_OK) -> None:
    assert response.status_code == expected_status
    assert template_name in (template.name for template in response.templates)


def assert_redirect(response: http.HttpResponse, redirect_url: str, *args: Any) -> None:
    assert response.status_code == status.HTTP_302_FOUND
    urls = response.url.split('?next=')
    assert urls[0] == redirect_url
    for follow_url, expected_follow_url in zip(urls[1:], args):
        assert follow_url == expected_follow_url


def assert_successful_json_response(response: http.JsonResponse, url: str) -> None:
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json['success'] == True
    assert json['url'] == url


def assert_data_present_in_json_response_html(response: http.HttpResponse, values) -> None:
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    for value in values:
        assert str(value) in json['html']


def assert_data_contains_fields(data: Dict, expected_fields: Iterable[str]) -> None:
    assert set(data) == set(expected_fields)


def assert_garden_connection_fields_are_updated(garden: Garden, response: str) -> None:
    assert garden.is_connected == True
    assert garden.last_connection_ip == response.wsgi_request.META.get('REMOTE_ADDR')
    assert datetime.now(pytz.UTC) - garden.last_connection_time < timedelta(seconds=1)


def assert_render_context_called_with(mock_render: Mock, kwarg: Dict) -> None:
    for key, item in kwarg.items():
        assert mock_render.call_args.kwargs['context'][key] == item
