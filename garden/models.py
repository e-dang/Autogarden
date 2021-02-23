from datetime import timedelta

from django.db import models


def _default_moisture_threshold():
    return 50


def _default_watering_duration():
    return timedelta(minutes=1)


def _default_garden_name():
    return 'My Garden'


class Garden(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255, default=_default_garden_name)


class WateringStation(models.Model):
    garden = models.ForeignKey(Garden, related_name='watering_stations', on_delete=models.CASCADE)
    moisture_threshold = models.IntegerField(default=_default_moisture_threshold)
    watering_duration = models.DurationField(default=_default_watering_duration)

    class Meta:
        ordering = ['id']
