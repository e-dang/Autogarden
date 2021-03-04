import pytest

from django.forms import ValidationError

from garden.forms import (REQUIRED_FIELD_ERR_MSG, NewGardenForm,
                          WateringStationForm)
from garden.models import Garden


@pytest.mark.integration
class TestNewGardenForm:
    @pytest.mark.parametrize('new_garden_form_fields, missing_field', [
        (None, 'name'),
        (None, 'num_watering_stations'),
        (None, 'update_interval')
    ],
        indirect=['new_garden_form_fields'],
        ids=['name', 'num_watering_stations', 'update_interval'])
    def test_fields_are_required(self, new_garden_form_fields, missing_field):
        new_garden_form_fields.pop(missing_field)
        form = NewGardenForm(data=new_garden_form_fields)

        assert not form.is_valid()
        assert form.errors[missing_field] == [REQUIRED_FIELD_ERR_MSG]

    @pytest.mark.django_db
    def test_save_creates_a_new_garden_with_specified_num_of_watering_stations(self, new_garden_form_fields, user):
        prev_num_gardens = Garden.objects.all().count()
        form = NewGardenForm(data=new_garden_form_fields)

        assert form.is_valid()
        garden = form.save(user)

        assert prev_num_gardens + 1 == Garden.objects.all().count()
        assert garden.watering_stations.count() == new_garden_form_fields['num_watering_stations']

    @pytest.mark.django_db
    def test_save_sets_new_garden_owner_as_passed_in_user(self, new_garden_form_fields, user):
        form = NewGardenForm(data=new_garden_form_fields)

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

    @pytest.mark.django_db
    def test_is_valid_returns_false_when_num_watering_stations_is_invalid(self, new_garden_form_fields):
        new_garden_form_fields['num_watering_stations'] = -1  # invalidate data
        form = NewGardenForm(data=new_garden_form_fields)

        ret_val = form.is_valid()

        assert ret_val == False
        assert NewGardenForm.NUM_WATERING_STATIONS_ERROR_MSG in form.errors['num_watering_stations']

    @pytest.mark.django_db
    def test_is_valid_returns_false_when_update_interval_is_invalid(self, new_garden_form_fields):
        new_garden_form_fields['update_interval'] = -1  # invalidate data
        form = NewGardenForm(data=new_garden_form_fields)

        ret_val = form.is_valid()

        assert ret_val == False
        assert NewGardenForm.UPDATE_INTERVAL_ERROR_MSG in form.errors['update_interval']


@pytest.mark.integration
class TestWateringStationForm:

    @pytest.mark.parametrize('watering_station_form_fields, missing_field', [
        (None, 'moisture_threshold'),
        (None, 'watering_duration')
    ],
        indirect=['watering_station_form_fields'],
        ids=['moisture_threshold', 'watering_duration'])
    def test_fields_are_required(self, watering_station_form_fields, missing_field):
        watering_station_form_fields.pop(missing_field)
        form = WateringStationForm(data=watering_station_form_fields)

        assert not form.is_valid()
        assert form.errors[missing_field] == [REQUIRED_FIELD_ERR_MSG]

    @pytest.mark.parametrize('watering_station_form_fields, missing_field', [
        (None, 'plant_type'),
        (None, 'status')
    ],
        indirect=['watering_station_form_fields'],
        ids=['plant_type', 'status'])
    def test_plant_type_field_is_not_required(self, watering_station_form_fields, missing_field):
        watering_station_form_fields.pop(missing_field)
        form = WateringStationForm(data=watering_station_form_fields)

        assert form.is_valid()
