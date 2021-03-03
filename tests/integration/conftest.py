from typing import Any

import pytest
from django import http
from pytest_factoryboy.fixture import LazyFixture
from rest_framework import status
from pytest_factoryboy import register
from tests import factories


@pytest.fixture
def auth_client_user(db, client, user1):
    """Cheap authenticated client and user tuple"""

    client.force_login(user1)
    yield client, user1


@pytest.fixture
def auth_client(auth_client_user):
    """Cheap authenticated client"""

    yield auth_client_user[0]


@pytest.fixture
def auth_user(auth_client_user):
    """Cheap authenticated user"""

    yield auth_client_user[1]


@pytest.fixture
def create_user(db, django_user_model, test_password):
    """Expensive user creation"""

    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'email' not in kwargs:
            kwargs['email'] = 'email@demo.com'
        return django_user_model.objects.create_user(**kwargs)
    yield make_user


@pytest.fixture
def true_auth_client_user(client, create_user, test_password):
    """Expensive authenticated client and user tuple"""

    user = create_user()
    client.login(email=user.email, password=test_password)
    yield client, user


@pytest.fixture
def true_auth_client(true_auth_client_user):
    """Expensive authenticated client"""

    yield true_auth_client_user[0]


@pytest.fixture
def true_auth_user(true_auth_client_user):
    """Expensive authenticated user"""

    yield true_auth_client_user[1]


register(factories.GardenFactory, 'auth_user_garden', owner=LazyFixture('auth_user'))


def assert_template_is_rendered(response: http.HttpResponse, template_name: str, expected_status: int = status.HTTP_200_OK) -> None:
    assert response.status_code == expected_status
    assert template_name in (template.name for template in response.templates)


def assert_redirect(response: http.HttpResponse, redirect_url: str, *args: Any) -> None:
    assert response.status_code == status.HTTP_302_FOUND
    urls = response.url.split('?next=')
    assert urls[0] == redirect_url
    for follow_url, expected_follow_url in zip(urls[1:], args):
        assert follow_url == expected_follow_url
