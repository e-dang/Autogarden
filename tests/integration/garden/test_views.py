import os
import random
from datetime import datetime, timedelta

import pytest
import pytz
from django import http
from rest_framework import status
from rest_framework.reverse import reverse
from tests.conftest import assert_image_files_equal
from tests.integration.conftest import (assert_redirect,
                                        assert_template_is_rendered)

from garden.forms import NewGardenForm
from garden.models import Garden, WateringStation
from garden.serializers import WateringStationSerializer
from garden.utils import derive_duration_string


def assert_successful_json_response(response: http.JsonResponse, url: str) -> None:
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json['success'] == True
    assert json['url'] == url


def assert_data_present_in_json_response_html(response: http.HttpResponse, values) -> None:
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    for value in values:
        assert str(value) in json['html']


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
    def test_GET_returns_garden_config_data(self, auth_api_client):
        resp = auth_api_client.get(self.url)

        assert resp.data['update_interval'] == self.garden.update_interval.total_seconds()

    @pytest.mark.django_db
    @pytest.mark.parametrize('water_level', [
        Garden.LOW,
        Garden.OK
    ],
        ids=['low', 'ok'])
    def test_PATCH_updates_the_garden_with_request_data(self, auth_api_client, water_level):
        self.garden.water_level = Garden.OK if water_level == Garden.LOW else Garden.LOW
        self.garden.save()
        data = {
            'water_level': water_level
        }

        auth_api_client.patch(self.url, data=data)

        self.garden.refresh_from_db()
        assert self.garden.water_level == data['water_level']

    @pytest.mark.django_db
    def test_PATCH_returns_204_status_code(self, auth_api_client):
        data = {
            'water_level': Garden.LOW
        }

        resp = auth_api_client.patch(self.url, data=data)

        assert resp.status_code == status.HTTP_204_NO_CONTENT

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
    def test_GET_updates_garden_connection_fields(self, auth_api_client):
        self.garden.is_connected = False

        resp = auth_api_client.get(self.url)

        self.garden.refresh_from_db()
        assert self.garden.is_connected == True
        assert self.garden.last_connection_ip == resp.wsgi_request.META.get('REMOTE_ADDR')
        assert datetime.now(pytz.UTC) - self.garden.last_connection_time < timedelta(seconds=1)

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

        assert_template_is_rendered(resp, 'garden_list.html')

    @pytest.mark.django_db
    def test_POST_with_valid_data_creates_new_garden_for_user_with_specified_num_watering_stations(self, auth_client, auth_user, valid_garden_data):
        prev_num_gardens = auth_user.gardens.all().count()

        auth_client.post(self.url, data=valid_garden_data)

        assert prev_num_gardens + 1 == auth_user.gardens.all().count()
        assert auth_user.gardens.last().watering_stations.count() == valid_garden_data['num_watering_stations']

    @pytest.mark.django_db
    def test_POST_with_valid_data_returns_json_response_with_success_and_redirect_url(self, auth_client, valid_garden_data):
        resp = auth_client.post(self.url, data=valid_garden_data, follow=False)

        assert_successful_json_response(resp, resp.wsgi_request.build_absolute_uri(reverse('garden-list')))

    @pytest.mark.django_db
    def test_POST_with_invalid_data_returns_json_response_with_failure_and_html(self, auth_client, invalid_new_garden_data):
        expected = [
            NewGardenForm.NUM_WATERING_STATIONS_ERROR_MSG
        ]

        resp = auth_client.post(self.url, data=invalid_new_garden_data)

        assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assert_redirect(resp, reverse('login'), self.url)


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

        assert_template_is_rendered(resp, 'garden_detail.html')

    @pytest.mark.django_db
    def test_GET_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden):
        url = self.create_url(garden.pk)

        resp = auth_client.get(url)

        assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client):
        resp = client.get(self.url, follow=False)

        assert_redirect(resp, reverse('login'), self.url)


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

        assert_template_is_rendered(resp, 'garden_update.html')

    @pytest.mark.django_db
    def test_POST_updates_garden_instance_fields(self, auth_client, valid_update_garden_data):
        auth_client.post(self.url, data=valid_update_garden_data)

        self.garden.refresh_from_db()
        assert self.garden.name == valid_update_garden_data['name']
        assert derive_duration_string(self.garden.update_interval) == valid_update_garden_data['update_interval']
        assert_image_files_equal(self.garden.image.url, valid_update_garden_data['image'].name)

    @pytest.mark.django_db
    def test_POST_returns_json_response_with_redirect_url_and_success_eq_true(self, auth_client, valid_update_garden_data):
        resp = auth_client.post(self.url, data=valid_update_garden_data)

        assert_successful_json_response(resp, self.url)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden, method):
        url = self.create_url(garden.pk)

        resp = getattr(auth_client, method)(url)

        assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_update_garden_when_accessed_by_user_who_doesnt_own_it(self, auth_client, garden, valid_update_garden_data):
        url = self.create_url(garden.pk)

        auth_client.post(url, data=valid_update_garden_data)

        garden.refresh_from_db()
        for key, item in valid_update_garden_data.items():
            assert getattr(garden, key) != item

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assert_redirect(resp, reverse('login'), self.url)


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
            f'action="{self.garden.get_delete_url()}"'
        ]

        resp = auth_client.get(self.garden.get_delete_url())

        assert_data_present_in_json_response_html(resp, expected)

    @pytest.mark.django_db
    def test_POST_deletes_the_specified_garden(self, auth_client):
        auth_client.post(self.garden.get_delete_url())

        with pytest.raises(Garden.DoesNotExist):
            self.garden.refresh_from_db()

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_list_page(self, auth_client):
        resp = auth_client.post(self.garden.get_delete_url())

        assert_redirect(resp, reverse('garden-list'))

    @pytest.mark.django_db
    @pytest.mark.usefixtures('use_tmp_static_dir')
    def test_POST_deletes_image_file_in_static_dir(self, auth_client):
        path = self.garden.get_abs_path_to_image()

        auth_client.post(self.garden.get_delete_url())

        assert not os.path.exists(path)

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden, method):
        url = self.create_url(garden.pk)

        resp = getattr(auth_client, method)(url)

        assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_does_not_delete_the_garden_when_access_by_user_who_doesnt_own_garden(self, auth_client, garden):
        url = self.create_url(garden.pk)

        auth_client.post(url)

        garden.refresh_from_db()  # should not raise

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assert_redirect(resp, reverse('login'), self.url)


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

        assert_template_is_rendered(resp, 'watering_station_detail.html')

    @pytest.mark.django_db
    def test_GET_redirects_users_who_dont_own_the_watering_station_to_404_page_not_found(self, auth_client, watering_station):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        resp = auth_client.get(url)

        assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client):
        resp = client.get(self.url, follow=False)

        assert_redirect(resp, reverse('login'), self.url)


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

        assert_template_is_rendered(resp, 'watering_station_update.html')

    @pytest.mark.django_db
    def test_POST_with_valid_data_returns_json_response_with_update_watering_station_form_html(self, auth_client, valid_watering_station_data):
        resp = auth_client.post(self.url, data=valid_watering_station_data)

        assert_data_present_in_json_response_html(resp, valid_watering_station_data.values())

    @pytest.mark.django_db
    def test_POST_with_valid_data_updates_the_watering_station_with_given_data(self, auth_client, valid_watering_station_data):
        resp = auth_client.post(self.url, data=valid_watering_station_data)

        self.watering_station.refresh_from_db()
        assert resp.status_code == status.HTTP_200_OK
        assert self.watering_station.moisture_threshold == valid_watering_station_data['moisture_threshold']
        assert derive_duration_string(
            self.watering_station.watering_duration) == valid_watering_station_data['watering_duration']
        assert self.watering_station.plant_type == valid_watering_station_data['plant_type']

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_watering_station_to_404_page_not_found(self, auth_client, watering_station, method):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        resp = getattr(auth_client, method)(url)

        assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_update_watering_station_is_accessed_by_user_who_doesnt_own_it(self, auth_client, watering_station, valid_watering_station_data):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        auth_client.post(url, data=valid_watering_station_data)

        watering_station.refresh_from_db()
        assert watering_station.moisture_threshold != valid_watering_station_data['moisture_threshold']
        assert derive_duration_string(
            watering_station.watering_duration) != valid_watering_station_data['watering_duration']
        assert watering_station.plant_type != valid_watering_station_data['plant_type']

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assert_redirect(resp, reverse('login'), self.url)


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

        assert_redirect(resp, self.garden.get_absolute_url())

    @pytest.mark.django_db
    def test_POST_creates_a_new_default_watering_station(self, auth_client):
        prev_num_watering_stations = self.garden.watering_stations.all().count()

        auth_client.post(self.url)

        assert prev_num_watering_stations + 1 == self.garden.watering_stations.count()

    @pytest.mark.django_db
    def test_POST_redirects_to_garden_detail(self, auth_client):
        resp = auth_client.post(self.url)

        assert_redirect(resp, self.garden.get_absolute_url())

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'patch'], ids=['post', 'patch'])
    def test_view_redirects_users_who_dont_own_the_garden_to_404_page_not_found(self, auth_client, garden, method):
        url = self.create_url(garden.pk)

        resp = getattr(auth_client, method)(url)

        assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_create_new_garden_is_requesting_user_does_not_own_garden(self, auth_client, garden, valid_watering_station_data):
        url = self.create_url(garden.pk)
        prev_num_watering_stations = garden.watering_stations.all().count()

        auth_client.post(url, data=valid_watering_station_data)

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

        assert_redirect(resp, reverse('login'), self.url)


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

        assert_data_present_in_json_response_html(resp, expected)

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

        assert_redirect(resp, reverse('garden-detail', kwargs={'pk': garden_pk}))

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_view_redirects_users_who_dont_own_the_watering_station_to_404_page_not_found(self, auth_client, watering_station, method):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        resp = getattr(auth_client, method)(url)

        assert_template_is_rendered(resp, '404.html', expected_status=status.HTTP_404_NOT_FOUND)

    @pytest.mark.django_db
    def test_POST_doesnt_delete_watering_station_is_accessed_by_user_who_doesnt_own_it(self, auth_client, watering_station):
        url = self.create_url(watering_station.garden.pk, watering_station.pk)

        auth_client.post(url)

        watering_station.refresh_from_db()  # should not raise

    @pytest.mark.parametrize('method', ['post', 'get'], ids=['post', 'get'])
    def test_logged_out_user_is_redirected_to_login_page_when_accessing_this_view(self, client, method):
        resp = getattr(client, method)(self.url, follow=False)

        assert_redirect(resp, reverse('login'), self.url)
