import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Column, HTML, Button, Field, Layout, Row,
                                 Submit)
from django import forms
from django.core.exceptions import ValidationError

from .models import Garden, WateringStation, _default_update_frequency
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
            HTML(self.MESSAGE),
            FormActions(
                Button('cancel', 'Cancel', css_class='btn-primary',
                       data_dismiss='modal', aria_hidden='true'),
                Submit('confirm_delete', 'Delete', css_class='btn-danger ml-2'),
                css_class="form-row justify-content-end"
            )
        )


class CropperMixin(forms.Form):
    CROP_BTN_ID = 'cropBtn'
    RESET_BTN_ID = 'resetBtn'
    IMAGE_CONTAINER_ID = 'imageContainer'
    BUTTON_CSS = 'btn-primary my-2'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cropper_fields = [
            Row(
                Column(
                    HTML(f'''
                <div class="row justify-content-center">
                    <div id="{self.IMAGE_CONTAINER_ID}" class="photo-container">
                    </div>
                </div>
            '''),
                )
            ),
            FormActions(

                Button('crop', 'Crop', css_id=self.CROP_BTN_ID,
                       css_class=self.BUTTON_CSS, hidden=True),
                Button('reset', 'Reset', css_id=self.RESET_BTN_ID,
                       css_class=self.BUTTON_CSS, hidden=True),
                css_class='form-row justify-content-center'
            ),
            HTML('<hr>')
        ]


class GardenForm(forms.ModelForm, CropperMixin):
    FORM_ID = 'gardenForm'
    MODAL_ID = 'deleteGardenModal'
    FORM_CONTAINER_ID = 'formContainer'

    update_frequency = CustomDurationField(validators=[validate_duration])

    class Meta:
        model = Garden
        fields = ['name', 'image', 'update_frequency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.FORM_ID
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'update_frequency',
            Row(
                Column(
                    Field('image', id='id_image'),
                )
            ),
            *self.cropper_fields,
            FormActions(
                Button('delete', 'Delete', css_class='btn btn-danger mr-2',
                       data_toggle='modal', data_target=f'#{self.MODAL_ID}'),
                Submit('submit', 'Update'),
                css_class="form-row justify-content-end"
            )
        )

        self.fields['update_frequency'].label = 'Update Frequency'


class NewGardenForm(GardenForm):
    FORM_ID = 'newGardenForm'
    MODAL_ID = 'newGardenModal'

    num_watering_stations = forms.IntegerField(label='Number of Watering Stations', validators=[
                                               MinValueValidator(0, MIN_VALUE_ERR_MSG)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = 'garden-list'
        self.helper.layout.insert(2, Field('num_watering_stations'))
        self.helper.layout[-1] = FormActions(
            Button('cancel', 'Cancel', css_class='btn-primary mr-2',
                   data_toggle='modal', data_target=f'#{self.MODAL_ID}'),
            Submit('submit', 'Create', css_class='btn-success'),
            css_class='form-row justify-content-end'
        )
        self.fields['update_frequency'].initial = _default_update_frequency()

    def save(self, owner):
        num_watering_stations = self.cleaned_data.pop('num_watering_stations')
        garden = owner.gardens.create(**self.cleaned_data)
        set_num_watering_stations(garden, num_watering_stations)
        return garden


class DeleteGardenForm(DeleteForm):
    FORM_ID = 'deleteGardenForm'
    MESSAGE = '<p>Are you sure you want to delete this garden?</p>'


class WateringStationForm(forms.ModelForm, CropperMixin):
    MODAL_ID = 'deleteWateringStationModal'
    FORM_ID = 'wateringStationForm'
    FORM_CONTAINER_ID = 'formContainer'

    watering_duration = CustomDurationField(validators=[validate_duration])
    moisture_threshold = forms.IntegerField(validators=[
        MinValueValidator(0, MIN_VALUE_ERR_MSG),
        MaxValueValidator(100, MAX_VALUE_ERR_MSG)
    ])

    class Meta:
        model = WateringStation
        fields = ['moisture_threshold', 'watering_duration', 'plant_type', 'status', 'image']
        error_messages = {
            'moisture_threshold': {'required': REQUIRED_FIELD_ERR_MSG},
            'watering_duration': {'required': REQUIRED_FIELD_ERR_MSG}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.FORM_ID
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('plant_type'),
            Field('moisture_threshold'),
            Field('watering_duration'),
            Field('status'),
            Field('image', id='id_image'),
            *self.cropper_fields,
            FormActions(
                Button('delete', 'Delete', css_class='btn btn-danger mr-2',
                       data_toggle='modal', data_target=f'#{self.MODAL_ID}'),
                Submit('submit', 'Update'),
                css_class="form-row justify-content-end"
            )
        )
        self.fields['status'].label = 'Enable'
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
