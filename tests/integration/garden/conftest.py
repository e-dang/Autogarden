import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from tests.conftest import TEST_IMAGE_DIR

from garden.utils import build_duration_string


@pytest.fixture
def valid_watering_station_data():
    return {'moisture_threshold': 89,
            'watering_duration': build_duration_string(5, 65),
            'plant_type': 'lettuce',
            'status': True
            }


@pytest.fixture
def valid_garden_data():
    return {'name': 'My Garden',
            'num_watering_stations': 3,
            'update_interval': '10:00'}


@pytest.fixture
def valid_update_garden_data(use_tmp_static_dir):
    image_path = str(TEST_IMAGE_DIR / 'test_garden_image.png')
    with open(image_path, 'rb') as f:
        file = SimpleUploadedFile('test_garden_image.png', f.read(), content_type='image/png')
        return {
            'name': 'new garden name',
            'update_interval': '10:00',
            'image': file
        }


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
