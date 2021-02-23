import uuid

import pytest
from django.db.utils import IntegrityError
from django.forms import ValidationError
from garden.forms import NewGardenForm
from garden.models import Garden
from garden.serializers import GardenSerializer, WateringStationSerializer
from rest_framework import status
from rest_framework.reverse import reverse


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


def is_template_rendered(template_name, response):
    return template_name in (template.name for template in response.templates)


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
    @pytest.mark.django_db
    def test_GET_renders_garden_html_template(self, client):
        url = reverse('garden-list')

        resp = client.get(url)

        assert resp.status_code == 200
        assert is_template_rendered('gardens.html', resp)

    @pytest.mark.django_db
    def test_POST_with_valid_data_creates_new_garden_record_with_specified_num_watering_stations(self, client):
        data = {'name': 'My Garden',
                'num_watering_stations': 3}
        url = reverse('garden-list')
        prev_num_gardens = Garden.objects.all().count()

        client.post(url, data=data)

        assert prev_num_gardens + 1 == Garden.objects.all().count()
        assert Garden.objects.first().watering_stations.count() == data['num_watering_stations']

    @pytest.mark.django_db
    def test_POST_with_valid_data_redirects_to_garden_list_page(self, client):
        data = {'name': 'My Garden',
                'num_watering_stations': 3}
        url = reverse('garden-list')

        resp = client.post(url, data=data, follow=False)

        assert resp.status_code == status.HTTP_302_FOUND
        assert resp.url == '/'


@pytest.mark.integration
class TestGardenModel:
    @pytest.mark.django_db
    def test_uuid_field_must_be_unique(self):
        id_ = uuid.uuid4()
        Garden(uuid=id_).save()

        with pytest.raises(IntegrityError) as err:
            Garden(uuid=id_).save()
            assert 'UNIQUE' in err


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
