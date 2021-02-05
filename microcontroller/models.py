from datetime import timedelta

from django.db import models


def _default_moisture_threshold():
    return 50


def _default_watering_duration():
    return timedelta(minutes=1)


class MicroController(models.Model):
    uuid = models.UUIDField(unique=True)


class WateringStation(models.Model):
    micro_controller = models.ForeignKey(MicroController, related_name='watering_stations', on_delete=models.CASCADE)
    moisture_threshold = models.IntegerField(default=_default_moisture_threshold)
    watering_duration = models.DurationField(default=_default_watering_duration)

    class Meta:
        ordering = ['id']
