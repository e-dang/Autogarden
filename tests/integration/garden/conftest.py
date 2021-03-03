import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse
from tests.conftest import TEST_IMAGE_DIR

from garden.utils import build_duration_string


@pytest.fixture
def data_POST_api_garden():
    num_watering_stations = 4
    url = reverse('api-garden')
    data = {
        'uuid': uuid.uuid4(),
        'num_watering_stations': num_watering_stations
    }

    return num_watering_stations, url, data


@pytest.fixture
def data_GET_api_watering_stations(garden_factory):
    num_watering_stations = 4
    garden = garden_factory(watering_stations=num_watering_stations)
    url = reverse('api-watering-stations', kwargs={'pk': garden.pk})

    return num_watering_stations, garden, url


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
