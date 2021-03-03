import pytest


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
