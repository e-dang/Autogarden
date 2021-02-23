from django import forms

from .models import Garden
from .utils import create_unique_garden_uuid, set_num_watering_stations


class NewGardenForm(forms.ModelForm):
    num_watering_stations = forms.IntegerField()

    class Meta:
        model = Garden
        fields = ['name']

    def clean_num_watering_stations(self):
        data = self.cleaned_data['num_watering_stations']
        if data < 0:
            raise forms.ValidationError('The number of watering stations must be positive')

        return data

    def save(self):
        uuid = create_unique_garden_uuid()
        garden = Garden.objects.create(name=self.cleaned_data['name'], uuid=uuid)
        set_num_watering_stations(garden, self.cleaned_data['num_watering_stations'])
        return garden
