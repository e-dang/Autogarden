import uuid

import pytest
from django import http
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.forms import ValidationError
from garden.forms import (REQUIRED_FIELD_ERR_MSG, NewGardenForm,
                          WateringStationForm)
from garden.models import Garden, WateringStation
from garden.serializers import GardenSerializer, WateringStationSerializer
from garden.utils import build_duration_string, derive_duration_string
from rest_framework import status
from rest_framework.reverse import reverse
from tests.conftest import TEST_IMAGE_DIR, assert_image_files_equal


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
            'num_watering_stations': 3}


@pytest.fixture
def valid_update_garden_data(use_tmp_static_dir):
    image_path = str(TEST_IMAGE_DIR / 'test_garden_image.png')
    with open(image_path, 'rb') as f:
        file = SimpleUploadedFile('test_garden_image.png', f.read(), content_type='image/png')
        return {
            'name': 'new garden name',
            'image': file
        }


def assert_template_is_rendered(response: http.HttpResponse, template_name: str):
    assert response.status_code == status.HTTP_200_OK
    assert template_name in (template.name for template in response.templates)


def assert_data_present_in_json_response_html(response: http.HttpResponse, values):
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    for value in values:
        assert str(value) in json['html']


def assert_redirect(response: http.HttpResponse, redirect_url: str):
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == redirect_url


@pytest.mark.integration
class TestAPIViews:
    @pytest.mark.parametrize('view, kwargs, expected', [
        ('api-garden', {}, '/api/garden/'),
        ('api-watering-stations', {'pk': 0}, '/api/garden/0/watering-stations/'),
    ],
        ids=['api-garden', 'garden'])
    def test_view_has_correct_url(self, view, kwargs, expected):
        assert reverse(view, kwargs=kwargs) == expected

    @pytest.mark.django_db
    def test_POST_api_garden_creates_garden_obj_with_specified_num_watering_stations(self, api_client, data_POST_api_garden):
        num_watering_stations, url, data = data_POST_api_garden

        api_client.post(url, data=data)

        assert Garden.objects.count() == 1
        garden = Garden.objects.get(uuid=data['uuid'])
        assert garden.watering_stations.count() == num_watering_stations

    @pytest.mark.django_db
    def test_POST_api_garden_returns_201_response_with_pk_data(self, api_client, data_POST_api_garden):
        _, url, data = data_POST_api_garden

        resp = api_client.post(url, data=data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data['pk'] == Garden.objects.get(uuid=data['uuid']).pk

    @pytest.mark.django_db
    def test_POST_api_garden_returns_409_response_if_garden_with_uuid_already_exists(self, api_client, garden_factory, data_POST_api_garden):
        _, url, data = data_POST_api_garden
        garden_factory(uuid=data['uuid'])

        resp = api_client.post(url, data=data)

        assert resp.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.django_db
    def test_POST_api_garden_returns_pk_of_garden_if_uuid_already_exists(self, api_client, garden_factory, data_POST_api_garden):
        _, url, data = data_POST_api_garden
        garden = garden_factory(uuid=data['uuid'])

        resp = api_client.post(url, data=data)

        assert int(resp.data['pk']) == garden.pk

    @pytest.mark.django_db
    def test_GET_api_watering_stations_returns_200_response(self, api_client, data_GET_api_watering_stations):
        _, _, url = data_GET_api_watering_stations

        resp = api_client.get(url)

        assert resp.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_GET_api_watering_stations_returns_serialized_watering_station_data_belonging_to_garden(self, api_client, data_GET_api_watering_stations):
        num_watering_stations, garden, url = data_GET_api_watering_stations

        resp = api_client.get(url)

        assert len(resp.data) == num_watering_stations
        watering_stations = list(garden.watering_stations.all())
        for i, watering_station in enumerate(resp.data):
            assert watering_station == WateringStationSerializer(watering_stations[i]).data


@pytest.mark.integration
class TestGardenListView:
    def test_view_has_correct_url(self):
        assert reverse('garden-list') == f'/gardens/'

    @pytest.fixture
    def url(self):
        return reverse('garden-list')

    @pytest.fixture
    def invalid_new_garden_data(self):
        return {'name': 'My Garden',
                'num_watering_stations': -1}

    @pytest.mark.django_db
    def test_GET_renders_garden_html_template(self, client, url):
        resp = client.get(url)

        assert_template_is_rendered(resp, 'garden_list.html')

    @pytest.mark.django_db
    def test_POST_with_valid_data_creates_new_garden_record_with_specified_num_watering_stations(self, client, url, valid_garden_data):
        prev_num_gardens = Garden.objects.all().count()

        client.post(url, data=valid_garden_data)

        assert prev_num_gardens + 1 == Garden.objects.all().count()
        assert Garden.objects.first().watering_stations.count() == valid_garden_data['num_watering_stations']

    @pytest.mark.django_db
    def test_POST_with_valid_data_returns_json_response_with_success_and_redirect_url(self, client, url, valid_garden_data):
        resp = client.post(url, data=valid_garden_data, follow=False)

        data = resp.json()
        assert data['success'] == True
        assert data['url'] == resp.wsgi_request.build_absolute_uri(reverse('garden-list'))

    @pytest.mark.django_db
    def test_POST_with_invalid_data_returns_json_response_with_failure_and_html(self, client, url, invalid_new_garden_data):
        resp = client.post(url, data=invalid_new_garden_data)

        data = resp.json()
        assert data['success'] == False
        assert NewGardenForm.NUM_WATERING_STATIONS_ERROR_MSG in data['html']


@pytest.mark.integration
class TestGardenDetailView:
    def test_view_has_correct_url(self):
        pk = 1
        assert reverse('garden-detail', kwargs={'pk': pk}) == f'/gardens/{pk}/'

    @pytest.mark.django_db
    def test_GET_renders_garden_detail_html_template(self, client, garden):
        resp = client.get(garden.get_absolute_url())

        assert_template_is_rendered(resp, 'garden_detail.html')


@pytest.mark.integration
class TestGardenUpdateView:
    @pytest.mark.django_db
    def test_GET_renders_garden_update_html_template(self, client, garden):
        resp = client.get(garden.get_update_url())

        assert_template_is_rendered(resp, 'garden_update.html')

    @pytest.mark.django_db
    def test_POST_updates_garden_instance_fields(self, client, garden, valid_update_garden_data):
        client.post(garden.get_update_url(), data=valid_update_garden_data)

        garden.refresh_from_db()
        assert garden.name == valid_update_garden_data['name']
        assert_image_files_equal(garden.image.url, valid_update_garden_data['image'].name)

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_update_view(self, client, garden, valid_update_garden_data):
        resp = client.post(garden.get_update_url(), data=valid_update_garden_data)

        assert_redirect(resp, garden.get_update_url())


@pytest.mark.integration
class TestGardenDeleteView:
    @pytest.mark.django_db
    def test_GET_returns_json_response_with_garden_delete_form_html(self, client, garden):
        expected = [
            'method="post"',
            f'action="{garden.get_delete_url()}"'
        ]

        resp = client.get(garden.get_delete_url())

        assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    def test_POST_deletes_the_specified_garden(self, client, garden):
        client.post(garden.get_delete_url())

        with pytest.raises(Garden.DoesNotExist):
            garden.refresh_from_db()

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_list_page(self, client, garden):
        resp = client.post(garden.get_delete_url())

        assert_redirect(resp, reverse('garden-list'))


@pytest.mark.integration
class TestWateringStationDetailView:
    @pytest.mark.django_db
    def test_GET_renders_watering_station_html_template(self, client, watering_station):
        resp = client.get(watering_station.get_absolute_url())

        assert_template_is_rendered(resp, 'watering_station.html')

    @pytest.mark.django_db
    def test_POST_with_valid_data_returns_json_response_with_update_watering_station_form_html(self, client, watering_station, valid_watering_station_data):
        resp = client.post(watering_station.get_absolute_url(), data=valid_watering_station_data)

        assert_data_present_in_json_response_html(resp, valid_watering_station_data.values())

    @pytest.mark.django_db
    def test_POST_with_valid_data_updates_the_watering_station_with_given_data(self, client, watering_station, valid_watering_station_data):
        resp = client.post(watering_station.get_absolute_url(), data=valid_watering_station_data)

        watering_station.refresh_from_db()
        assert resp.status_code == status.HTTP_200_OK
        assert watering_station.moisture_threshold == valid_watering_station_data['moisture_threshold']
        assert derive_duration_string(
            watering_station.watering_duration) == valid_watering_station_data['watering_duration']
        assert watering_station.plant_type == valid_watering_station_data['plant_type']


@pytest.mark.integration
class TestWateringStationListView:
    @pytest.mark.django_db
    def test_PATCH_updates_all_watering_stations_for_a_given_garden_with_the_data(self, client, garden):
        data = {'status': False}

        client.patch(garden.get_watering_stations_url(), data=data)

        for station in garden.watering_stations.all():
            assert station.status == data['status']

    @pytest.mark.django_db
    def test_PATCH_redirects_to_garden_detail_page(self, client, garden):
        data = {'status': False}

        resp = client.patch(garden.get_watering_stations_url(), data=data)

        assert_redirect(resp, garden.get_absolute_url())

    @pytest.mark.django_db
    def test_POST_creates_a_new_default_watering_station(self, client, garden):
        prev_num_watering_stations = garden.watering_stations.count()

        client.post(garden.get_watering_stations_url())

        assert prev_num_watering_stations + 1 == garden.watering_stations.count()

    @pytest.mark.django_db
    def test_POST_redicrects_to_garden_detail(self, client, garden):
        resp = client.post(garden.get_watering_stations_url())

        assert_redirect(resp, garden.get_absolute_url())


@pytest.mark.integration
class TestWateringStationDeleteView:
    @pytest.mark.django_db
    def test_GET_returns_json_response_with_form_html_that_posts_to_watering_station_delete(self, client, watering_station):
        expected = [
            'method="post"',
            f'action="{watering_station.get_delete_url()}"'
        ]

        resp = client.get(watering_station.get_delete_url())

        assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    def test_POST_deletes_watering_station_with_given_pk(self, client, watering_station):
        ws_pk = watering_station.pk
        client.post(watering_station.get_delete_url())

        with pytest.raises(WateringStation.DoesNotExist):
            WateringStation.objects.get(pk=ws_pk)

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_detail_view(self, client, watering_station):
        garden_pk = watering_station.garden.pk

        resp = client.post(watering_station.get_delete_url())

        assert_redirect(resp, reverse('garden-detail', kwargs={'pk': garden_pk}))


@pytest.mark.integration
class TestGardenModel:
    @pytest.mark.django_db
    def test_uuid_field_must_be_unique(self):
        id_ = uuid.uuid4()
        Garden(uuid=id_).save()

        with pytest.raises(IntegrityError) as err:
            Garden(uuid=id_).save()
            assert 'UNIQUE' in err

    @pytest.mark.django_db
    @pytest.mark.parametrize('garden_factory, nulled_data', [
        (None, {'last_connection_ip': None}),
        (None, {'last_connection_time': None}),
        (None, {'water_level': None})
    ],
        indirect=['garden_factory'],
        ids=['last_connection_ip', 'last_connection_time', 'water_level'])
    def test_fields_can_be_null_field(self, garden_factory, nulled_data):
        garden_factory(**nulled_data)  # should not raise

    @pytest.mark.django_db
    def test_get_absolute_url_returns_correct_url(self, garden):
        url = garden.get_absolute_url()

        assert url == f'/gardens/{garden.pk}/'

    @pytest.mark.django_db
    def test_get_watering_station_urls(self, garden):
        url = garden.get_watering_stations_url()

        assert url == f'/gardens/{garden.pk}/watering-stations/'

    @pytest.mark.django_db
    def test_get_update_url_returns_correct_url(self, garden):
        url = garden.get_update_url()

        assert url == f'/gardens/{garden.pk}/update/'

    @pytest.mark.django_db
    def test_get_delete_url_returns_correct_url(self, garden):
        url = garden.get_delete_url()

        assert url == f'/gardens/{garden.pk}/delete/'


@pytest.mark.integration
class TestGardenSerializer:
    @pytest.mark.django_db
    def test_serializer_requires_num_watering_stations(self):
        serializer = GardenSerializer(data={'uuid': uuid.uuid4()})

        assert serializer.is_valid() is False
        assert serializer.errors['num_watering_stations'][0].code == 'required'

    @pytest.mark.django_db
    def test_create_adds_num_watering_stations_to_garden_instance(self):
        num_watering_stations = 16
        serializer = GardenSerializer()

        garden = serializer.create({'uuid': uuid.uuid4(), 'num_watering_stations': num_watering_stations})

        assert garden.watering_stations.count() == num_watering_stations


@pytest.mark.integration
class TestNewGardenForm:
    @pytest.mark.parametrize('valid_garden_data, missing_field', [
        (None, 'name'),
        (None, 'num_watering_stations'),
    ],
        indirect=['valid_garden_data'],
        ids=['name', 'num_watering_stations'])
    def test_fields_are_required(self, valid_garden_data, missing_field):
        valid_garden_data.pop(missing_field)
        form = NewGardenForm(data=valid_garden_data)

        assert not form.is_valid()
        assert form.errors[missing_field] == [REQUIRED_FIELD_ERR_MSG]

    @pytest.mark.django_db
    def test_save_creates_a_new_garden_with_specified_num_of_watering_stations(self):
        data = {
            'name': 'My Garden',
            'num_watering_stations': 4
        }
        prev_num_gardens = Garden.objects.all().count()
        form = NewGardenForm(data=data)

        assert form.is_valid()
        garden = form.save()

        assert prev_num_gardens + 1 == Garden.objects.all().count()
        assert garden.watering_stations.count() == data['num_watering_stations']

    @pytest.mark.django_db
    def test_clean_num_watering_stations_raises_validation_error_when_number_is_negative(self):
        data = {
            'name': 'My Garden',
            'num_watering_stations': -1
        }
        form = NewGardenForm(data=data)
        form.cleaned_data = data

        with pytest.raises(ValidationError):
            form.clean_num_watering_stations()


@pytest.mark.integration
class TestWateringStationModel:
    @pytest.mark.django_db
    def test_get_absolute_url_returns_correct_url(self, watering_station):
        garden = watering_station.garden

        url = watering_station.get_absolute_url()

        assert url == f'/gardens/{garden.pk}/watering-stations/{watering_station.pk}/'

    @pytest.mark.django_db
    def test_get_delete_url_returns_correct_url(self, watering_station):
        garden = watering_station.garden

        url = watering_station.get_delete_url()

        assert url == f'/gardens/{garden.pk}/watering-stations/{watering_station.pk}/delete/'


@pytest.mark.integration
class TestWateringStationForm:

    @pytest.mark.parametrize('valid_watering_station_data, missing_field', [
        (None, 'moisture_threshold'),
        (None, 'watering_duration')
    ],
        indirect=['valid_watering_station_data'],
        ids=['moisture_threshold', 'watering_duration'])
    def test_fields_are_required(self, valid_watering_station_data, missing_field):
        valid_watering_station_data.pop(missing_field)
        form = WateringStationForm(data=valid_watering_station_data)

        assert not form.is_valid()
        assert form.errors[missing_field] == [REQUIRED_FIELD_ERR_MSG]

    @pytest.mark.parametrize('valid_watering_station_data, missing_field', [
        (None, 'plant_type'),
        (None, 'status')
    ],
        indirect=['valid_watering_station_data'],
        ids=['plant_type', 'status'])
    def test_plant_type_field_is_not_required(self, valid_watering_station_data, missing_field):
        valid_watering_station_data.pop(missing_field)
        form = WateringStationForm(data=valid_watering_station_data)

        assert form.is_valid()
