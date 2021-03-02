import shutil

import pytest
from django.conf import settings
from garden.models import _default_garden_image
from pytest_factoryboy import register
from rest_framework.test import APIClient
from selenium import webdriver

from . import factories

TEST_IMAGE_DIR = settings.BASE_DIR / 'tests' / 'images'

register(factories.GardenFactory)
register(factories.WateringStationFactory)
register(factories.WateringStationRecordFactory)
register(factories.UserFactory)


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', default=False)


@pytest.fixture(scope='session')
def faker_seed():
    return 12345


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


@pytest.fixture
def test_password():
    return factories.TEST_PASSWORD


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'email' not in kwargs:
            kwargs['email'] = 'email@demo.com'
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user(password=test_password)
            client.login(email=user.email, password=test_password)
            return client, user

    return make_auto_login


@pytest.fixture
def use_tmp_static_dir(settings, tmp_path):
    image_name = _default_garden_image()
    src_path = settings.BASE_DIR / 'garden' / 'static' / 'images' / image_name
    static_dir = tmp_path / 'static'
    static_dir.mkdir()
    image_dir = static_dir / 'images'
    image_dir.mkdir()
    dest_path = image_dir / image_name
    shutil.copyfile(src_path, dest_path)
    settings.STATIC_ROOT = static_dir
    settings.MEDIA_ROOT = image_dir


def assert_image_files_equal(image_path1, image_path2):
    assert image_path1.split('/')[-1] == image_path2.split('/')[-1]
