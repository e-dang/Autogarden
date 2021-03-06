from typing import Any, Dict
from unittest.mock import Mock

from django import http
from rest_framework import status


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


def assert_render_context_called_with(mock_render: Mock, kwarg: Dict) -> None:
    for key, item in kwarg.items():
        assert mock_render.call_args.kwargs['context'][key] == item
