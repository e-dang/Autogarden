from django import http
from rest_framework import status
from typing import Any


def assert_template_is_rendered(response: http.HttpResponse, template_name: str) -> None:
    assert response.status_code == status.HTTP_200_OK
    assert template_name in (template.name for template in response.templates)


def assert_redirect(response: http.HttpResponse, redirect_url: str, *args: Any) -> None:
    assert response.status_code == status.HTTP_302_FOUND
    urls = response.url.split('?next=')
    assert urls[0] == redirect_url
    for follow_url, expected_follow_url in zip(urls[1:], args):
        assert follow_url == expected_follow_url
