import os
import random
from datetime import datetime, timedelta
from random import randint

import pytest
import pytz
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from tests import assertions

from garden.forms import MIN_VALUE_ERR_MSG, REQUIRED_FIELD_ERR_MSG
from garden.models import Garden, WateringStation
from garden.serializers import GardenGetSerializer, WateringStationSerializer
from garden.utils import derive_duration_string


@pytest.mark.integration
def test_home_redirects_to_garden_list_view(auth_client):
    url = reverse('home')

    resp = auth_client.get(url)

    assertions.assert_redirect(resp, reverse('garden-list'))


@pytest.mark.integration
class TestGardenAPIView:
    @pytest.fixture(autouse=True)
    def setup(self, auth_api_garden):
        self.garden = auth_api_garden
        self.url = reverse('api-garden', kwargs={'pk': auth_api_garden.pk})

    @pytest.mark.django_db
    def test_view_has_correct_url(self):
        assert self.url == f'/api/gardens/{self.garden.pk}/'

    @pytest.mark.django_db
    def test_GET_returns_200_status_code(self, auth_api_client):
        resp = auth_api_client.get(self.url)

        assert resp.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_GET_returns_data_with_correct_fields(self, auth_api_client):
        resp = auth_api_client.get(self.url)

        assertions.assert_unordered_data_eq(resp.data, GardenGetSerializer.Meta.fields)

    @pytest.mark.django_db
    def test_GET_returns_garden_config_data(self, auth_api_client):
        resp = auth_api_client.get(self.url)

        assert len(resp.data) == 1  # reminder to update field equality assertions if adding another serializer field
        assert resp.data['update_frequency'] == self.garden.update_frequency.total_seconds()

    @pytest.mark.django_db
    def test_PATCH_updates_the_garden_with_request_data(self, auth_api_client, garden_patch_serializer_data):
        self.garden.water_level = Garden.OK if garden_patch_serializer_data['water_level'] == Garden.LOW else Garden.LOW
        self.garden.save()

        auth_api_client.patch(self.url, data=garden_patch_serializer_data)

        self.garden.refresh_from_db()
        field_equality = [
            getattr(self.garden, field) == value for field, value in garden_patch_serializer_data.items()
        ]
        assert all(field_equality)

    @pytest.mark.django_db
    def test_PATCH_updates_garden_connection_fields(self, auth_api_client, garden_patch_serializer_data):
        self.garden.is_connected = False
        self.garden.save()

        resp = auth_api_client.patch(self.url, data=garden_patch_serializer_data)

        self.garden.refresh_from_db()
        assertions.assert_garden_connection_fields_are_updated(self.garden, resp)

    @pytest.mark.django_db
    def test_PATCH_returns_204_status_code(self, auth_api_client, garden_patch_serializer_data):
        resp = auth_api_client.patch(self.url, data=garden_patch_serializer_data)

        assert resp.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_PATCH_with_invalid_data_returns_400_status_code(self, auth_api_client, garden_invalid_patch_serializer_data):
        resp = auth_api_client.patch(self.url, data=garden_invalid_patch_serializer_data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_PATCH_with_missing_field_returns_400_status_code(self, auth_api_client, garden_missing_patch_serializer_data):
        data, field = garden_missing_patch_serializer_data

        resp = auth_api_client.patch(self.url, data=data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assertions.assert_serializer_required_field_error(resp.data[field])

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['get', 'patch'], ids=['get', 'patch'])
    def test_accessing_api_without_authorization_token_returns_403_response(self, api_client, method):
        resp = getattr(api_client, method)(self.url)

        assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.integration
class TestWateringStationAPIView:
    @pytest.fixture(autouse=True)
    def setup(self, auth_api_garden):
        self.garden = auth_api_garden
        self.url = reverse('api-watering-stations', kwargs={'pk': self.garden.pk})

    def test_view_has_correct_url(self):
        assert self.url == f'/api/gardens/{self.garden.pk}/watering-stations/'

    @pytest.mark.django_db
    def test_GET_returns_200_response(self, auth_api_client):
        resp = auth_api_client.get(self.url)

        assert resp.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_GET_returns_serialized_watering_station_data_belonging_to_garden(self, auth_api_client):
        num_watering_stations = self.garden.watering_stations.all().count()

        resp = auth_api_client.get(self.url)

        assert len(resp.data) == num_watering_stations
        watering_stations = list(self.garden.watering_stations.all())
        for i, watering_station in enumerate(resp.data):
            assert watering_station == WateringStationSerializer(watering_stations[i]).data

    @pytest.mark.django_db
    def test_POST_adds_a_watering_station_record_to_each_watering_station_in_garden(self, auth_api_client):
        data = []
        num_watering_stations = self.garden.watering_stations.all().count()
        for _ in range(num_watering_stations):
            data.append({
                'moisture_level': random.uniform(0, 100)
            })

        auth_api_client.post(self.url, data=data, format='json')

        for record, station in zip(data, self.garden.watering_stations.all()):
            assert station.records.all().count() == 1
            station.records.get(moisture_level=record['moisture_level'])

    @pytest.mark.django_db
    def test_POST_returns_201_status_code(self, auth_api_client):
        data = []
        num_watering_stations = self.garden.watering_stations.all().count()
        for _ in range(num_watering_stations):
            data.append({
                'moisture_level': random.uniform(0, 100)
            })

        resp = auth_api_client.post(self.url, data=data, format='json')

        assert resp.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['get', 'post'], ids=['get', 'post'])
    def test_accessing_api_without_authorization_token_returns_403_response(self, api_client, method):
        resp = getattr(api_client, method)(self.url)

        assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.integration
class TestGardenListView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = reverse('garden-list')

    def test_view_has_correct_url(self):
        assert self.url == f'/gardens/'

    @pytest.fixture
    def invalid_new_garden_data(self):
        return {'name': 'My Garden',
                'num_watering_stations': -1}

    @pytest.mark.django_db
    def test_GET_renders_garden_html_template(self, auth_client):
        resp = auth_client.get(self.url)

        assertions.assert_template_is_rendered(resp, 'garden_list.html')

    @pytest.mark.django_db
    def test_POST_with_valid_data_creates_new_garden_for_user_with_specified_num_watering_stations(self, auth_client, auth_user, new_garden_form_fields):
        prev_num_gardens = auth_user.gardens.all().count()

        auth_client.post(self.url, data=new_garden_form_fields)

        assert prev_num_gardens + 1 == auth_user.gardens.all().count()
        assert auth_user.gardens.last().watering_stations.count() == new_garden_form_fields['num_watering_stations']

    @pytest.mark.django_db
    def test_POST_with_valid_data_returns_json_response_with_success_and_redirect_url(self, auth_client, new_garden_form_fields):
        resp = auth_client.post(self.url, data=new_garden_form_fields, follow=False)

        assertions.assert_successful_json_response(resp, resp.wsgi_request.build_absolute_uri(reverse('garden-list')))

    @pytest.mark.django_db
    def test_POST_with_invalid_data_returns_json_response_with_failure_and_html(self, auth_client, invalid_new_garden_data):
        expected = [
            MIN_VALUE_ERR_MSG
        ]

        resp = auth_client.post(self.url, data=invalid_new_garden_data)

        assertions.assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestGardenDetailView:
    def create_url(self, pk):
        return reverse('garden-detail', kwargs={'pk': pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_garden):
        self.garden = auth_user_garden
        self.url = self.create_url(self.garden.pk)

    @pytest.mark.django_db
    def test_view_has_correct_url(self):
        assert self.url == f'/gardens/{self.garden.pk}/'

    @pytest.mark.django_db
    def test_GET_renders_garden_detail_html_template(self, auth_client):
        resp = auth_client.get(self.url)

        assertions.assert_template_is_rendered(resp, 'garden_detail.html')

    @pytest.mark.django_db
    def test_GET_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden):
        url = self.create_url(garden.pk)

        resp = auth_client.get(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client):
        resp = client.get(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestGardenUpdateView:
    def create_url(self, pk):
        return reverse('garden-update', kwargs={'pk': pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_garden):
        self.garden = auth_user_garden
        self.url = self.create_url(self.garden.pk)

    @pytest.mark.django_db
    def test_view_has_correct_url(self):
        assert self.url == f'/gardens/{self.garden.pk}/update/'

    @pytest.mark.django_db
    def test_GET_renders_garden_update_html_template(self, auth_client):
        resp = auth_client.get(self.url)

        assertions.assert_template_is_rendered(resp, 'garden_update.html')

    @pytest.mark.django_db
    def test_POST_updates_garden_instance_fields(self, auth_client, update_garden_form_fields):
        auth_client.post(self.url, data=update_garden_form_fields)

        self.garden.refresh_from_db()
        assert self.garden.name == update_garden_form_fields['name']
        assert self.garden.update_frequency == update_garden_form_fields['update_frequency']
        assertions.assert_image_files_equal(self.garden.image.url, update_garden_form_fields['image'].name)

    @pytest.mark.django_db
    def test_POST_returns_json_response_with_redirect_url_and_success_eq_true(self, auth_client, update_garden_form_fields):
        resp = auth_client.post(self.url, data=update_garden_form_fields)

        assertions.assert_successful_json_response(resp, self.url)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden, method):
        url = self.create_url(garden.pk)

        resp = getattr(auth_client, method)(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_update_garden_when_accessed_by_user_who_doesnt_own_it(self, auth_client, garden1, update_garden_form_fields):
        url = self.create_url(garden1.pk)

        auth_client.post(url, data=update_garden_form_fields)

        garden1.refresh_from_db()
        assert any(
            getattr(garden1, key) != item for key, item in update_garden_form_fields.items()
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestGardenDeleteView:
    def create_url(self, pk):
        return reverse('garden-delete', kwargs={'pk': pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_garden):
        self.garden = auth_user_garden
        self.url = self.create_url(self.garden.pk)

    @pytest.mark.django_db
    def test_GET_returns_json_response_with_garden_delete_form_html(self, auth_client):
        expected = [
            'method="post"',
            f'action="{self.url}"'
        ]

        resp = auth_client.get(self.url)

        assertions.assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    def test_POST_deletes_the_specified_garden(self, auth_client):
        auth_client.post(self.url)

        with pytest.raises(Garden.DoesNotExist):
            self.garden.refresh_from_db()

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_list_page(self, auth_client):
        resp = auth_client.post(self.url)

        assertions.assert_redirect(resp, reverse('garden-list'))

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.usefixtures('use_tmp_static_dir')
    def test_POST_deletes_image_file_in_static_dir(self, auth_client, update_garden_form_fields):
        self.garden.image = update_garden_form_fields['image']
        self.garden.save()
        self.garden.refresh_from_db()
        path = settings.STATIC_ROOT
        for segment in self.garden.image.url.split('/'):
            path /= segment

        auth_client.post(self.url)

        assert not os.path.exists(path)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden, method):
        url = self.create_url(garden.pk)

        resp = getattr(auth_client, method)(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_does_not_delete_the_garden_when_access_by_user_who_doesnt_own_garden(self, auth_client, garden):
        url = self.create_url(garden.pk)

        auth_client.post(url)

        garden.refresh_from_db()  # should not raise

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestWateringStationDetailView:
    def create_url(self, garden_pk, ws_pk):
        return reverse('watering-station-detail',
                       kwargs={'garden_pk': garden_pk, 'ws_pk': ws_pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_ws):
        self.watering_station = auth_user_ws
        self.garden = auth_user_ws.garden
        self.url = self.create_url(self.garden.pk, self.watering_station.pk)

    @pytest.mark.django_db
    def test_view_has_correct_url(self):
        assert self.url == f'/gardens/{self.garden.pk}/watering-stations/{self.watering_station.pk}/'

    @pytest.mark.django_db
    def test_GET_renders_watering_station_detail_html_template(self, auth_client):
        resp = auth_client.get(self.url)

        assertions.assert_template_is_rendered(resp, 'watering_station_detail.html')

    @pytest.mark.django_db
    def test_GET_redirects_users_who_dont_own_the_watering_station_to_404_page_not_found(self, auth_client, watering_station):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        resp = auth_client.get(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client):
        resp = client.get(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestWateringStationUpdateView:
    def create_url(self, garden_pk, ws_pk):
        return reverse('watering-station-update',
                       kwargs={'garden_pk': garden_pk, 'ws_pk': ws_pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_ws):
        self.watering_station = auth_user_ws
        self.garden = auth_user_ws.garden
        self.url = self.create_url(self.garden.pk, self.watering_station.pk)

    @pytest.mark.django_db
    def test_GET_renders_watering_station_update_html_template(self, auth_client):
        resp = auth_client.get(self.url)

        assertions.assert_template_is_rendered(resp, 'watering_station_update.html')

    @pytest.mark.django_db
    def test_POST_with_valid_data_returns_json_response_with_url_to_redirect_to_and_success_eq_true(self, auth_client, watering_station_form_fields):
        resp = auth_client.post(self.url, data=watering_station_form_fields)

        assertions.assert_successful_json_response(resp, self.url)

    @pytest.mark.django_db
    def test_POST_with_valid_data_updates_the_watering_station_with_given_data(self, auth_client, watering_station_form_fields):
        resp = auth_client.post(self.url, data=watering_station_form_fields)

        self.watering_station.refresh_from_db()
        assert resp.status_code == status.HTTP_200_OK
        assert self.watering_station.moisture_threshold == watering_station_form_fields['moisture_threshold']
        assert derive_duration_string(
            self.watering_station.watering_duration) == watering_station_form_fields['watering_duration']
        assert self.watering_station.plant_type == watering_station_form_fields['plant_type']

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_watering_station_to_404_page_not_found(self, auth_client, watering_station, method):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        resp = getattr(auth_client, method)(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_update_watering_station_is_accessed_by_user_who_doesnt_own_it(self, auth_client, watering_station, watering_station_form_fields):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        auth_client.post(url, data=watering_station_form_fields)

        watering_station.refresh_from_db()
        assert any([
            watering_station.moisture_threshold != watering_station_form_fields['moisture_threshold'],
            derive_duration_string(
                watering_station.watering_duration) != watering_station_form_fields['watering_duration'],
            watering_station.plant_type != watering_station_form_fields['plant_type']
        ])

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestWateringStationListView:
    def create_url(self, pk):
        return reverse('watering-station-list', kwargs={'pk': pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_garden):
        self.garden = auth_user_garden
        self.url = self.create_url(self.garden.pk)

    @pytest.mark.django_db
    def test_view_has_correct_url(self):
        assert self.url == f'/gardens/{self.garden.pk}/watering-stations/'

    @pytest.mark.django_db
    def test_PATCH_updates_all_watering_stations_for_a_given_garden_with_the_data(self, auth_client):
        data = {'status': False}

        auth_client.patch(self.url, data=data)

        for station in self.garden.watering_stations.all():
            assert station.status == data['status']

    @pytest.mark.django_db
    def test_PATCH_redirects_to_garden_detail_page(self, auth_client):
        data = {'status': False}

        resp = auth_client.patch(self.url, data=data)

        assertions.assert_redirect(resp, self.garden.get_absolute_url())

    @pytest.mark.django_db
    def test_POST_creates_a_new_default_watering_station(self, auth_client):
        prev_num_watering_stations = self.garden.watering_stations.all().count()

        auth_client.post(self.url)

        assert prev_num_watering_stations + 1 == self.garden.watering_stations.count()

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_detail(self, auth_client):
        resp = auth_client.post(self.url)

        assertions.assert_redirect(resp, self.garden.get_absolute_url())

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'patch'], ids=['post', 'patch'])
    def test_view_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden, method):
        url = self.create_url(garden.pk)

        resp = getattr(auth_client, method)(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_create_new_garden_is_requesting_user_does_not_own_garden(self, auth_client, garden, watering_station_form_fields):
        url = self.create_url(garden.pk)
        prev_num_watering_stations = garden.watering_stations.all().count()

        auth_client.post(url, data=watering_station_form_fields)

        garden.refresh_from_db()
        assert prev_num_watering_stations == garden.watering_stations.all().count()

    @pytest.mark.django_db
    def test_PATCH_doesnt_update_garden_watering_stations_if_requesting_user_does_not_own_garden(self, auth_client, garden1):
        url = self.create_url(garden1.pk)
        prev_status = True
        station = garden1.watering_stations.first()
        station.status = prev_status
        station.save()

        auth_client.patch(url, data={'status': not prev_status})

        station.refresh_from_db()
        assert station.status == prev_status

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'patch'], ids=['post', 'patch'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestWateringStationDeleteView:
    def create_url(self, garden_pk, ws_pk):
        return reverse('watering-station-delete',
                       kwargs={'garden_pk': garden_pk, 'ws_pk': ws_pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_ws):
        self.watering_station = auth_user_ws
        self.garden = auth_user_ws.garden
        self.url = self.create_url(self.garden.pk, self.watering_station.pk)

    @pytest.mark.django_db
    def test_GET_returns_json_response_with_form_html_that_posts_to_watering_station_delete(self, auth_client):
        expected = [
            'method="post"',
            f'action="{self.url}"'
        ]

        resp = auth_client.get(self.url)

        assertions.assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    def test_POST_deletes_watering_station_with_given_pk(self, auth_client):
        ws_pk = self.watering_station.pk
        auth_client.post(self.url)

        with pytest.raises(WateringStation.DoesNotExist):
            WateringStation.objects.get(pk=ws_pk)

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_detail_view(self, auth_client):
        garden_pk = self.garden.pk

        resp = auth_client.post(self.url)

        assertions.assert_redirect(resp, reverse('garden-detail', kwargs={'pk': garden_pk}))

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_watering_station_to_404_page_not_found(self, auth_client, watering_station, method):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        resp = getattr(auth_client, method)(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_delete_watering_station_is_accessed_by_user_who_doesnt_own_it(self, auth_client, watering_station):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        auth_client.post(url)

        watering_station.refresh_from_db()  # should not raise

    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assertions.assert_redirect(resp, reverse('login'), self.url)


@pytest.mark.integration
class TestWateringStationRecordListView:
    def create_url(self, garden_pk, ws_pk):
        return reverse('watering-station-record-list', kwargs={'garden_pk': garden_pk, 'ws_pk': ws_pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_ws):
        self.garden = auth_user_ws.garden
        self.watering_station = auth_user_ws
        self.url = self.create_url(self.garden.pk, self.watering_station.pk)

    @pytest.mark.django_db
    def test_GET_returns_json_response_with_watering_station_records_from_the_last_12_hours(self, auth_client):
        num_records = 14
        update_frequency = timedelta(hours=1)
        self.watering_station.update_frequency = update_frequency
        time_created = datetime.now(pytz.UTC) - update_frequency * num_records
        expected_records = []
        for _ in range(num_records):
            record = self.watering_station.records.create(moisture_level=float(randint(0, 100)))
            record.created = time_created
            record.save()
            if datetime.now(pytz.UTC) - time_created < timedelta(hours=12):
                expected_records.append(record)
            time_created += update_frequency

        resp = auth_client.get(self.url)
        json = resp.json()

        assert len(json['labels']) == len(expected_records)
        assert len(json['data']) == len(expected_records)
        assert set(json['data']) == set(record.moisture_level for record in expected_records)

    @pytest.mark.django_db
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client):
        resp = client.get(self.url)

        assertions.assert_redirect(resp, reverse('login'), self.url)

    @pytest.mark.django_db
    def test_GET_returns_404_page_when_accessed_by_user_who_doesnt_own_the_watering_station(self, auth_client, watering_station):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        resp = auth_client.get(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_GET_returns_404_page_when_accessing_a_resource_that_doesnt_exist(self, auth_client):
        num_watering_stations = self.garden.watering_stations.all().count()
        url = self.create_url(self.garden.pk, num_watering_stations + 1)

        resp = auth_client.get(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)


@pytest.mark.integration
class TestWateringStationCreateView:
    def create_url(self, pk):
        return reverse('watering-station-create', kwargs={'pk': pk})

    @pytest.fixture(autouse=True)
    def setup(self, auth_user_garden):
        self.garden = auth_user_garden
        self.url = self.create_url(self.garden.pk)

    def test_view_has_correct_url(self):
        assert self.url == f'/gardens/{self.garden.pk}/watering-stations/create/'

    @pytest.mark.django_db
    def test_GET_returns_json_response_with_NewWateringStation_form_html(self, auth_client, watering_station_form_fields):
        expected = watering_station_form_fields.keys()

        resp = auth_client.get(self.url)

        assertions.assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    def test_POST_with_valid_data_creates_a_new_watering_station_instance_on_garden(self, auth_client, watering_station_form_fields):
        prev_num_watering_stations = self.garden.watering_stations.count()

        auth_client.post(self.url, data=watering_station_form_fields)

        self.garden.refresh_from_db()
        assert self.garden.watering_stations.count() == prev_num_watering_stations + 1

    @pytest.mark.django_db
    def test_POST_with_valid_data_creates_new_watering_station_with_supplied_data(self, auth_client, watering_station_form_fields):
        auth_client.post(self.url, data=watering_station_form_fields)

        self.garden.refresh_from_db()
        watering_station = self.garden.watering_stations.last()
        assert watering_station_form_fields.pop(
            'watering_duration') == derive_duration_string(watering_station.watering_duration)
        assertions.assert_model_fields_have_values(watering_station_form_fields, watering_station)

    @pytest.mark.django_db
    def test_POST_with_valid_data_returns_json_response_with_a_redirect_url_and_success_true_field(self, auth_client, watering_station_form_fields):
        resp = auth_client.post(self.url, data=watering_station_form_fields)

        assertions.assert_successful_json_response(resp, reverse('garden-detail', kwargs={'pk': self.garden.pk}))

    @pytest.mark.django_db
    def test_POST_with_invalid_data_returns_json_response_with_form_errors_and_success_false_field(self, auth_client, watering_station_form_fields):
        watering_station_form_fields.pop('watering_duration')  # invalidate data
        expected = [
            REQUIRED_FIELD_ERR_MSG
        ]

        resp = auth_client.post(self.url, data=watering_station_form_fields)

        assertions.assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['get', 'post'], ids=['get', 'post'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url)

        assertions.assert_redirect(resp, reverse('login'), self.url)

    @pytest.mark.django_db
    def test_GET_returns_404_page_when_accessed_by_user_who_doesnt_own_the_garden(self, auth_client, garden):
        url = self.create_url(garden.pk)

        resp = auth_client.get(url)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_returns_404_page_when_accessed_by_user_who_doesnt_own_the_garden(self, auth_client, garden, watering_station_form_fields):
        url = self.create_url(garden.pk)

        resp = auth_client.post(url, data=watering_station_form_fields)

        assertions.assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)
