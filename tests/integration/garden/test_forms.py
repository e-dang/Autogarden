

import pytest

from django.forms import ValidationError

from garden.forms import (REQUIRED_FIELD_ERR_MSG, NewGardenForm,
                          WateringStationForm)
from garden.models import Garden


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
    def test_save_creates_a_new_garden_with_specified_num_of_watering_stations(self, valid_garden_data, user):
        prev_num_gardens = Garden.objects.all().count()
        form = NewGardenForm(data=valid_garden_data)

        assert form.is_valid()
        garden = form.save(user)

        assert prev_num_gardens + 1 == Garden.objects.all().count()
        assert garden.watering_stations.count() == valid_garden_data['num_watering_stations']

    @pytest.mark.django_db
    def test_save_sets_new_garden_owner_as_passed_in_user(self, valid_garden_data, user):
        form = NewGardenForm(data=valid_garden_data)

        assert form.is_valid()
        garden = form.save(user)

        assert garden in user.gardens.all()

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
