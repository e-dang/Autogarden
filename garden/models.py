from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse
import pytz

from .utils import derive_duration_string


def _default_moisture_threshold():
    return 50


def _default_watering_duration():
    return timedelta(minutes=1)


def _default_garden_name():
    return 'My Garden'


def _default_is_connected():
    return False


def _default_update_interval():
    return timedelta(minutes=5)


def _default_num_missed_updates():
    return 0


CONNECTED_STR = 'Connected'
DISCONNECTED_STR = 'Disconnected'


class Garden(models.Model):
    OK = 'ok'
    LOW = 'lo'
    WATER_LEVEL_CHOICES = [
        (OK, 'Ok'),
        (LOW, 'Low'),
    ]

    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255, default=_default_garden_name)
    is_connected = models.BooleanField(default=_default_is_connected)
    last_connection_ip = models.GenericIPAddressField(null=True)
    last_connection_time = models.DateTimeField(null=True)
    update_interval = models.DurationField(default=_default_update_interval)
    num_missed_updates = models.PositiveIntegerField(default=_default_num_missed_updates)
    water_level = models.CharField(choices=WATER_LEVEL_CHOICES, max_length=2, null=True)

    def get_absolute_url(self):
        return reverse('garden-detail', kwargs={'pk': self.pk})

    @property
    def status(self):
        return CONNECTED_STR if self.is_connected else DISCONNECTED_STR

    def calc_time_till_next_update(self):
        if self.last_connection_time is None:
            return None
        factor = 1
        next_update = self.last_connection_time + factor * self.update_interval - datetime.now(pytz.UTC)
        while next_update.total_seconds() < 0:
            factor += 1
            next_update = self.last_connection_time + factor * self.update_interval - datetime.now(pytz.UTC)
        return int(next_update.total_seconds())

    def get_formatted_last_connection_time(self):
        if self.last_connection_time is None:
            return str(None)
        return self.last_connection_time.strftime('%-m/%d/%Y %I:%M %p')


class WateringStation(models.Model):
    garden = models.ForeignKey(Garden, related_name='watering_stations', on_delete=models.CASCADE)
    moisture_threshold = models.IntegerField(default=_default_moisture_threshold)
    watering_duration = models.DurationField(default=_default_watering_duration)
    plant_type = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('watering-station-detail', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    def get_formatted_duration(self):
        return derive_duration_string(self.watering_duration)
