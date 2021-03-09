from datetime import datetime, timedelta

import pytest
import pytz

from garden.formatters import WateringStationFormatter
from garden.models import Garden, Token, WateringStation


@pytest.mark.integration
class TestGardenModel:
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

    @pytest.mark.django_db
    def test_token_object_is_auto_created_when_garden_is_created(self, user):
        garden = Garden(owner=user)
        garden.save()

        assert isinstance(garden.token, Token)

    @pytest.mark.django_db
    def test_garden_is_not_deleted_when_token_is_delete(self, garden):
        garden.token.delete()

        garden.refresh_from_db()

        with pytest.raises(Garden.token.RelatedObjectDoesNotExist):
            garden.token

    @pytest.mark.django_db
    def test_garden_is_not_deleted_when_watering_station_is_delete(self, garden1):
        watering_station = garden1.watering_stations.first()
        watering_station.delete()

        garden1.refresh_from_db()

        with pytest.raises(WateringStation.DoesNotExist):
            watering_station.refresh_from_db()

    @pytest.mark.django_db
    def test_garden_is_deleted_when_user_is_delete(self, user1):
        garden = user1.gardens.first()

        user1.delete()

        with pytest.raises(Garden.DoesNotExist):
            garden.refresh_from_db()

    @pytest.mark.django_db
    def test_refresh_connection_status_updates_is_connected_if_update_hasnt_happened_within_the_update_frequency(self, garden):
        garden.is_connected = True
        garden.last_connection_time = datetime.now(pytz.UTC) - timedelta(minutes=10)
        garden.update_frequency = timedelta(minutes=5)
        garden.save()

        garden.refresh_connection_status()

        assert garden.is_connected == False

    @pytest.mark.django_db
    @pytest.mark.parametrize('is_connected', [True, False], ids=['true', 'false'])
    def test_refresh_connection_status_doesnt_do_anything_if_last_connection_time_is_none(self, garden, is_connected):
        garden.is_connected = is_connected
        garden.last_connection_time = None
        garden.save()

        garden.refresh_connection_status()

        assert garden.is_connected == is_connected

    @pytest.mark.django_db
    def test_refresh_connection_status_sets_connection_strength_to_none_if_update_hasnt_happened_within_the_update_frequency(self, garden):
        garden.connection_strength = -1
        garden.last_connection_time = datetime.now(pytz.UTC) - timedelta(minutes=10)
        garden.update_frequency = timedelta(minutes=5)
        garden.save()

        garden.refresh_connection_status()

        assert garden.connection_strength is None

    @pytest.mark.django_db
    def test_get_watering_station_formatters_returns_all_watering_stations_wrapped_in_a_formatter(self, garden):
        formatter_ids = set()
        for station in garden.get_watering_station_formatters():
            formatter_ids.add(station.pk)
            assert isinstance(station, WateringStationFormatter)


@pytest.mark.integration
class TestTokenModel:
    @pytest.mark.django_db
    def test_token_is_deleted_when_garden_is_deleted(self, garden):
        token = garden.token

        garden.delete()

        with pytest.raises(Token.DoesNotExist):
            token.refresh_from_db()


@pytest.mark.integration
class TestWateringStationModel:

    @pytest.mark.django_db
    def test_get_absolute_url_returns_correct_url(self, watering_station):
        garden = watering_station.garden

        url = watering_station.get_absolute_url()

        assert url == f'/gardens/{garden.pk}/watering-stations/{watering_station.pk}/'

    @pytest.mark.django_db
    def test_get_update_url_returns_correct_url(self, watering_station):
        garden = watering_station.garden

        url = watering_station.get_update_url()

        assert url == f'/gardens/{garden.pk}/watering-stations/{watering_station.pk}/update/'

    @pytest.mark.django_db
    def test_get_delete_url_returns_correct_url(self, watering_station):
        garden = watering_station.garden

        url = watering_station.get_delete_url()

        assert url == f'/gardens/{garden.pk}/watering-stations/{watering_station.pk}/delete/'

    @pytest.mark.django_db
    def test_get_records_url_returns_the_correct_url(self, watering_station):
        garden = watering_station.garden

        url = watering_station.get_records_url()

        assert url == f'/gardens/{garden.pk}/watering-stations/{watering_station.pk}/records/'

    @pytest.mark.django_db
    def test_watering_station_gets_deleted_when_garden_gets_delete(self, watering_station):
        garden = watering_station.garden

        garden.delete()

        with pytest.raises(WateringStation.DoesNotExist):
            watering_station.refresh_from_db()
