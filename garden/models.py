import os
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db import models
from django.urls import reverse
from PIL import Image
from rest_framework.request import Request

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


def _default_status():
    return True


def _default_garden_image():
    return 'default_garden.png'


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
    image = models.ImageField(default=_default_garden_image)
    is_connected = models.BooleanField(default=_default_is_connected)
    last_connection_ip = models.GenericIPAddressField(null=True)
    last_connection_time = models.DateTimeField(null=True)
    update_interval = models.DurationField(default=_default_update_interval)
    num_missed_updates = models.PositiveIntegerField(default=_default_num_missed_updates)
    water_level = models.CharField(choices=WATER_LEVEL_CHOICES, max_length=2, null=True)

    def get_absolute_url(self):
        return reverse('garden-detail', kwargs={'pk': self.pk})

    def get_watering_stations_url(self):
        return reverse('watering-station-list', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('garden-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('garden-delete', kwargs={'pk': self.pk})

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

    def delete(self, *args, **kwargs):
        try:
            if _default_garden_image() not in self.image.url:
                os.remove(self.get_abs_path_to_image())
        except OSError:
            pass
        super().delete(*args, **kwargs)

    def get_abs_path_to_image(self):
        path = settings.STATIC_ROOT
        for segment in self.image.url.split('/'):
            path /= segment
        return path

    def update(self, request: Request):
        self.is_connected = True
        self.last_connection_ip = request.META.get('REMOTE_ADDR')
        self.last_connection_time = datetime.now(pytz.UTC)
        self.save()


class WateringStation(models.Model):
    ACTIVE_STATUS_STR = 'Active'
    INACTIVE_STATUS_STR = 'Inactive'

    garden = models.ForeignKey(Garden, related_name='watering_stations', on_delete=models.CASCADE)
    moisture_threshold = models.IntegerField(default=_default_moisture_threshold)
    watering_duration = models.DurationField(default=_default_watering_duration)
    plant_type = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=_default_status)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('watering-station-detail', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    def get_delete_url(self):
        return reverse('watering-station-delete', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    def get_formatted_duration(self):
        return derive_duration_string(self.watering_duration)

    @property
    def status_string(self):
        return self.ACTIVE_STATUS_STR if self.status else self.INACTIVE_STATUS_STR


class WateringStationRecord(models.Model):
    watering_station = models.ForeignKey(WateringStation, related_name='records', on_delete=models.CASCADE)
    moisture_level = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
