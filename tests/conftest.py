import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from . import factories


@pytest.fixture(scope='session')
def faker_seed():
    return 12345


@pytest.fixture
def api_client():
    return APIClient()


register(factories.MicroControllerFactory)
register(factories.WateringStationFactory)
