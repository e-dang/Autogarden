import pytest
from django.conf import settings
from pytest_factoryboy import register
from rest_framework.test import APIClient
from selenium import webdriver

from . import factories

TEST_IMAGE_DIR = settings.BASE_DIR / 'tests' / 'images'

register(factories.GardenFactory)
register(factories.WateringStationFactory)


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', default=False)


@pytest.fixture(scope='class')
def driver_init(request):
    if request.config.getoption('--headless'):
        opts = webdriver.FirefoxOptions()
        opts.add_argument('--headless')
        request.cls.driver = webdriver.Firefox(options=opts)
    else:
        request.cls.driver = webdriver.Firefox()

    yield

    request.cls.driver.quit()


@pytest.fixture(scope='session')
def faker_seed():
    return 12345


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def use_tmp_static_dir(settings, tmp_path_factory):
    settings.MEDIA_ROOT = tmp_path_factory.getbasetemp()


def assert_image_files_equal(image_path1, image_path2):
    assert image_path1.split('/')[-1] == image_path2.split('/')[-1]
