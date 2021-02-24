from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Garden
from .utils import create_unique_garden_uuid, set_num_watering_stations

NEW_GARDEN_FORM_ID = 'newGardenForm'
NEW_GARDEN_SUBMIT_ID = 'submitBtn'

NUM_WATERING_STATIONS_ERROR_MSG = 'The number of watering stations must be positive'


class NewGardenForm(forms.ModelForm):
    num_watering_stations = forms.IntegerField(label="Number of Watering Stations")

    class Meta:
        model = Garden
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = NEW_GARDEN_FORM_ID
        self.helper.form_method = 'post'
        self.helper.form_action = 'garden-list'
        self.helper.add_input(Submit('submit', 'Create', css_id=NEW_GARDEN_SUBMIT_ID))

    def clean_num_watering_stations(self):
        data = self.cleaned_data['num_watering_stations']
        if data < 0:
            raise forms.ValidationError(NUM_WATERING_STATIONS_ERROR_MSG)

        return data

    def save(self):
        uuid = create_unique_garden_uuid()
        garden = Garden.objects.create(name=self.cleaned_data['name'], uuid=uuid)
        set_num_watering_stations(garden, self.cleaned_data['num_watering_stations'])
        return garden
