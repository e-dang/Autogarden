import pytest
from django.test import Client
from pytest_factoryboy import register
from pytest_factoryboy.fixture import LazyFixture
from tests import factories


@pytest.fixture(autouse=True)
def fast_hasher(settings):
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture
def auth_client_user(db, user1):
    """Cheap authenticated client and user tuple"""
    client = Client()
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


@pytest.fixture
def auth_user_garden(auth_user, garden_factory):
    yield garden_factory(owner=auth_user)


register(factories.WateringStationFactory, 'auth_user_ws', garden=LazyFixture('auth_user_garden'))
