from random import randint

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from tests.conftest import TEST_IMAGE_DIR


@pytest.fixture
def watering_station_form_fields(watering_station_factory):
    return watering_station_factory.form_fields()


@pytest.fixture
def new_garden_form_fields(garden_factory):
    data = garden_factory.form_fields()
    data['num_watering_stations'] = randint(0, 10)
    return data


@pytest.fixture
def valid_update_garden_data(garden_factory, use_tmp_static_dir):
    image_path = str(TEST_IMAGE_DIR / 'test_garden_image.png')
    with open(image_path, 'rb') as f:
        data = garden_factory.form_fields()
        data['image'] = SimpleUploadedFile('test_garden_image.png', f.read(), content_type='image/png')
        return data


@pytest.fixture
def auth_api_client_garden(db, garden_factory):
    api_client = APIClient()
    garden = garden_factory(watering_stations=3)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + garden.token.uuid)
    yield api_client, garden


@pytest.fixture
def auth_api_client(auth_api_client_garden):
    yield auth_api_client_garden[0]


@pytest.fixture
def auth_api_garden(auth_api_client_garden):
    yield auth_api_client_garden[1]
