from datetime import datetime, timedelta

import pytest
import pytz
from django.db.utils import IntegrityError
from tests.assertions import assert_unordered_data_eq

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

    @pytest.mark.django_db
    @pytest.mark.parametrize('garden__watering_stations, idx', [
        (4, 2)
    ])
    def test_get_watering_station_idx_returns_the_idx_of_the_watering_station_out_of_the_gardens_watering_stations(self, garden, idx):
        station = list(garden.watering_stations.all())[idx]

        ret_val = garden.get_watering_station_idx(station)

        assert ret_val == idx

    @pytest.mark.django_db
    @pytest.mark.parametrize('garden__watering_stations', [4])
    @pytest.mark.parametrize('idx', [0, 1, 2, 3], ids=[0, 1, 2, 3])
    def test_get_watering_station_at_idx_returns_correct_watering_station(self, garden, idx):
        ret_val = garden.get_watering_station_at_idx(idx)

        assert ret_val == list(garden.watering_stations.all())[idx]

    @pytest.mark.django_db
    def test_get_watering_station_formatters_returns_generator_of_formatters_for_each_watering_station(self, garden2):
        for formatter, station in zip(garden2.get_watering_station_formatters(), garden2.watering_stations.all()):
            assert isinstance(formatter, WateringStationFormatter)
            assert formatter.instance == station

    @pytest.mark.django_db
    def test_get_active_watering_stations_returns_only_watering_stations_that_are_active(self, garden, watering_station_factory):
        watering_stations = []
        for i in range(10):
            status = i % 2 == 0
            station = watering_station_factory(garden=garden, status=status)
            if status:
                watering_stations.append(station)

        ret_val = garden.get_active_watering_stations()

        assert list(ret_val) == watering_stations

    @pytest.mark.django_db
    def test_get_num_active_watering_stations_returns_number_of_active_watering_stations(self, garden, watering_station_factory):
        watering_stations = []
        for i in range(10):
            status = i % 2 == 0
            station = watering_station_factory(garden=garden, status=status)
            if status:
                watering_stations.append(station)

        ret_val = garden.get_num_active_watering_stations()

        assert ret_val == len(watering_stations)

    @pytest.mark.django_db
    def test_plant_types_returns_an_iterable_of_the_unique_plant_types_defined_in_its_watering_stations(self, garden, watering_station_factory):
        plant_types = ['lettuce', 'spinach']
        watering_station_factory(garden=garden, plant_type='')
        for i in range(5):
            plant_type = plant_types[0] if i % 2 == 0 else plant_types[1]
            watering_station_factory(garden=garden, plant_type=plant_type)

        ret_val = garden.plant_types

        assert_unordered_data_eq(ret_val, plant_types)

    @pytest.mark.django_db
    def test_a_user_cannot_have_two_gardens_with_the_same_name(self, user, garden_factory):
        garden_name = 'New Garden'
        garden_factory(owner=user, name=garden_name)

        with pytest.raises(IntegrityError):
            garden_factory(owner=user, name=garden_name)


@pytest.mark.integration
class TestTokenModel:
    @pytest.mark.django_db
    def test_token_is_deleted_when_garden_is_deleted(self, garden):
        token = garden.token

        garden.delete()

        with pytest.raises(Token.DoesNotExist):
            token.refresh_from_db()

    @pytest.mark.django_db
    def test_verify_returns_true_when_valid_token_is_passed_in(self, token_factory):
        uuid = 'random uuid'
        token = token_factory(uuid=uuid)

        ret_val = token.verify(uuid)

        assert ret_val == True

    @pytest.mark.django_db
    def test_verify_returns_false_when_invalid_token_is_passed_in(self, token_factory):
        uuid = 'random uuid'
        token = token_factory(uuid=uuid)

        ret_val = token.verify(uuid + 'random chars')

        assert ret_val == False


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

    @pytest.mark.django_db
    @pytest.mark.parametrize('num_watering_stations', [5], ids=[5])
    def test_idx_returns_the_correct_idx_within_the_garden(self, watering_station_factory, watering_station, num_watering_stations):
        watering_stations = [watering_station]
        for _ in range(num_watering_stations - 1):
            watering_stations.append(watering_station_factory(garden=watering_station.garden))

        for i, station in enumerate(watering_stations):
            assert station.idx == i

    @pytest.mark.django_db
    def test_watering_stations_are_kept_in_the_order_they_are_created(self, watering_station_factory, garden):
        watering_stations = []
        for _ in range(5):
            watering_stations.append(watering_station_factory(garden=garden))

        ret_val = list(garden.watering_stations.all())

        assert watering_stations == ret_val
