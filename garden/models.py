from datetime import timedelta

from django.db import models
from django.urls import reverse


def _default_moisture_threshold():
    return 50


def _default_watering_duration():
    return timedelta(minutes=1)


def _default_garden_name():
    return 'My Garden'


class Garden(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255, default=_default_garden_name)

    def get_absolute_url(self):
        return reverse('garden-detail', kwargs={'pk': self.pk})


class WateringStation(models.Model):
    garden = models.ForeignKey(Garden, related_name='watering_stations', on_delete=models.CASCADE)
    moisture_threshold = models.IntegerField(default=_default_moisture_threshold)
    watering_duration = models.DurationField(default=_default_watering_duration)
    plant_type = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('watering-station-detail', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})
