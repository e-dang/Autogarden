import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, Field, Layout,
                                 Submit)
from django import forms
from django.core.exceptions import ValidationError

from .models import Garden, WateringStation, _default_update_interval
from .utils import (derive_duration_string,
                    set_num_watering_stations)
from django.core.validators import MinValueValidator, MaxValueValidator

REQUIRED_FIELD_ERR_MSG = 'This field is required.'
INVALID_DURATION_ERR_MSG = 'This field must contain a duration greater than 1 second.'
MIN_VALUE_ERR_MSG = 'This field must be positve.'
MAX_VALUE_ERR_MSG = 'This field must be less than or equal to 100.'


def validate_duration(duration):
    if duration.total_seconds() < 1:
        raise ValidationError(INVALID_DURATION_ERR_MSG)


class CustomDurationField(forms.DurationField):
    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            return derive_duration_string(value)
        return value


class DeleteForm(forms.Form):
    FORM_ID = None
    MESSAGE = None

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.FORM_ID
        self.helper.method = 'post'
        self.helper.layout = Layout(
            FormActions(
                HTML(self.MESSAGE),
                Button('cancel', 'Cancel', css_class='btn btn-info',
                       data_dismiss='modal', aria_hidden='true'),
                Submit('confirm_delete', 'Delete', css_class='btn btn-danger'),
            )
        )


class CropperMixin(forms.Form):
    CROP_BTN_ID = 'cropBtn'
    RESET_BTN_ID = 'resetBtn'
    IMAGE_CONTAINER_ID = 'imageContainer'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cropper_fields = [
            HTML(f'''
                <div id="{self.IMAGE_CONTAINER_ID}">
                </div>
            '''),
            Button('crop', 'Crop', css_id=self.CROP_BTN_ID, hidden=True),
            Button('reset', 'Reset', css_id=self.RESET_BTN_ID, hidden=True)
        ]


class NewGardenForm(forms.ModelForm, CropperMixin):
    FORM_ID = 'newGardenForm'
    MODAL_ID = 'newGardenModal'

    num_watering_stations = forms.IntegerField(label='Number of Watering Stations', validators=[
                                               MinValueValidator(0, MIN_VALUE_ERR_MSG)])
    update_interval = CustomDurationField(validators=[validate_duration])

    class Meta:
        model = Garden
        fields = ['name', 'image', 'update_interval']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.FORM_ID
        self.helper.form_method = 'post'
        self.helper.form_action = 'garden-list'
        self.helper.layout = Layout(
            Field('name'),
            Field('update_interval'),
            Field('num_watering_stations', ),
            Field('image', id='id_image'),
            *self.cropper_fields,
            Submit('submit', 'Create', css_class='btn btn-success'),
            Button('cancel', 'Cancel', css_class='btn btn-info',
                   data_toggle='modal', data_target=f'#{self.MODAL_ID}')
        )

        self.fields['update_interval'].initial = _default_update_interval()

    def save(self, owner):
        num_watering_stations = self.cleaned_data.pop('num_watering_stations')
        garden = owner.gardens.create(**self.cleaned_data)
        set_num_watering_stations(garden, num_watering_stations)
        return garden


class UpdateGardenForm(forms.ModelForm, CropperMixin):
    FORM_ID = 'updateGardenForm'
    MODAL_ID = 'deleteGardenModal'
    FORM_CONTAINER_ID = 'formContainer'

    update_interval = CustomDurationField()

    class Meta:
        model = Garden
        fields = ['name', 'image', 'update_interval']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.FORM_ID
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name'),
            Field('update_interval'),
            Field('image', id='id_image'),
            *self.cropper_fields,
            Submit('submit', 'Update'),
            Button('delete', 'Delete', css_class='btn btn-danger',
                   data_toggle='modal', data_target=f'#{self.MODAL_ID}')
        )


class DeleteGardenForm(DeleteForm):
    FORM_ID = 'deleteGardenForm'
    MESSAGE = '<p>Are you sure you want to delete this garden?</p>'


class WateringStationForm(forms.ModelForm):
    MODAL_ID = 'deleteWateringStationModal'
    MOISTURE_THRESHOLD_ERR_MSG = 'The moisture threshold must be in the range 0 - 100.'

    watering_duration = CustomDurationField(validators=[validate_duration])
    moisture_threshold = forms.IntegerField(validators=[
        MinValueValidator(0, MIN_VALUE_ERR_MSG),
        MaxValueValidator(100, MAX_VALUE_ERR_MSG)
    ])

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
        self.helper.add_input(Submit('submit', 'Update'))
        self.helper.add_input(Button('delete', 'Delete', css_class='btn btn-danger',
                                     data_toggle='modal', data_target=f'#{self.MODAL_ID}'))

        self.fields['moisture_threshold'].label = 'Moisture Threshold'
        self.fields['watering_duration'].label = 'Watering Duration'


class BulkUpdateWateringStationForm(WateringStationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class DeleteWateringStationForm(DeleteForm):
    FORM_ID = 'deleteWateringStationForm'
    MESSAGE = '<p>Are you sure you want to delete this watering station?</p>'
