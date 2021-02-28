import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder, Field, Layout,
                                 Submit)
from django import forms

from .models import Garden, WateringStation
from .utils import (create_unique_garden_uuid, derive_duration_string,
                    set_num_watering_stations)

REQUIRED_FIELD_ERR_MSG = 'This field is required.'


class NewGardenForm(forms.ModelForm):
    NUM_WATERING_STATIONS_ERROR_MSG = 'The number of watering stations must be positive'
    NEW_GARDEN_FORM_ID = 'newGardenForm'
    NEW_GARDEN_SUBMIT_ID = 'submitBtn'

    num_watering_stations = forms.IntegerField(label="Number of Watering Stations")

    class Meta:
        model = Garden
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.NEW_GARDEN_FORM_ID
        self.helper.form_method = 'post'
        self.helper.form_action = 'garden-list'
        self.helper.add_input(Submit('submit', 'Create', css_id=self.NEW_GARDEN_SUBMIT_ID))

    def clean_num_watering_stations(self):
        data = self.cleaned_data['num_watering_stations']
        if data < 0:
            raise forms.ValidationError(self.NUM_WATERING_STATIONS_ERROR_MSG)

        return data

    def save(self):
        uuid = create_unique_garden_uuid()
        garden = Garden.objects.create(name=self.cleaned_data['name'], uuid=uuid)
        set_num_watering_stations(garden, self.cleaned_data['num_watering_stations'])
        return garden


class UpdateGardenForm(forms.ModelForm):
    SUBMIT_BTN_ID = 'submitBtn'
    DELETE_BTN_ID = 'deleteBtn'
    DELETE_GARDEN_MODAL_ID = 'deleteGardenModal'

    class Meta:
        model = Garden
        fields = ['name', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name'),
            Field('image', id='id_image'),
            Submit('submit', 'Update', css_id=self.SUBMIT_BTN_ID),
            Button('delete', 'Delete', css_id=self.DELETE_BTN_ID, css_class='btn btn-danger',
                   data_toggle='modal', data_target=f'#{self.DELETE_GARDEN_MODAL_ID}')
        )


class DeleteGardenForm(forms.Form):
    CONFIRM_DELETE_BTN_ID = 'confirmDeleteBtn'
    CANCEL_DELETE_BTN_ID = 'cancelDeleteBtn'

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.helper = FormHelper()
        self.method = 'post'
        self.helper.layout = Layout(
            FormActions(
                HTML('<p>Are you sure you want to delete this garden?</p>'),
                Button('cancel', 'Cancel', css_id=self.CANCEL_DELETE_BTN_ID, css_class='btn btn-info',
                       data_dismiss='modal', aria_hidden='true'),
                Submit('submit', 'Delete', css_id=self.CONFIRM_DELETE_BTN_ID, css_class='btn btn-danger'),
            )
        )


class CustomDurationField(forms.DurationField):
    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            return derive_duration_string(value)
        return value


class WateringStationForm(forms.ModelForm):
    UPDATE_WATERING_STATION_SUBMIT_ID = 'submitBtn'
    DELETE_WATERING_STATION_MODAL_ID = 'deleteWateringStationModal'
    DELETE_BUTTON_ID = 'deleteButton'

    watering_duration = CustomDurationField()

    class Meta:
        model = WateringStation
        fields = ['moisture_threshold', 'watering_duration', 'plant_type', 'status']
        error_messages = {
            'moisture_threshold': {'required': REQUIRED_FIELD_ERR_MSG},
            'watering_duration': {'required': REQUIRED_FIELD_ERR_MSG}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'updateWateringStationForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update', css_id=self.UPDATE_WATERING_STATION_SUBMIT_ID))
        self.helper.add_input(Button('delete', 'Delete', css_id=self.DELETE_BUTTON_ID, css_class='btn btn-danger',
                                     data_toggle='modal', data_target=f'#{self.DELETE_WATERING_STATION_MODAL_ID}'))

        self.fields['moisture_threshold'].label = 'Moisture Threshold'
        self.fields['watering_duration'].label = 'Watering Duration'


class BulkUpdateWateringStationForm(WateringStationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class DeleteWateringStationForm(forms.Form):
    CANCEL_DELETE_BTN_ID = 'cancelDeleteBtn'
    CONFIRM_DELETE_BTN_ID = 'confirmDeleteBtn'
    FORM_ID = 'deleteWateringStationForm'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.FORM_ID
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<p>Are you sure you want to delete this watering station?</p>'),
            ButtonHolder(
                Button('cancel', 'Cancel', css_id=self.CANCEL_DELETE_BTN_ID, css_class='btn btn-info',
                       data_dismiss='modal', aria_hidden='true'),
                Submit('submit', 'Delete', css_id=self.CONFIRM_DELETE_BTN_ID, css_class='btn btn-danger')
            )
        )
