from django import forms

from .models import Garden


class NewGardenForm(forms.ModelForm):
    num_watering_stations = forms.IntegerField()

    class Meta:
        model = Garden
        fields = ['name']
