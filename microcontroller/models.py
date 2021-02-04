from django.db import models

from .managers import MicroControllerManager


class MicroController(models.Model):
    uuid = models.UUIDField(unique=True)

    objects = MicroControllerManager()


class WateringStation(models.Model):
    micro_controller = models.ForeignKey(MicroController, related_name='watering_stations', on_delete=models.CASCADE)
