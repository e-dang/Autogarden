import uuid
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db import models
from django.urls import reverse
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

    # Values from https://www.speedcheck.org/wiki/rssi/#:~:text=RSSI%20or%20this%20signal%20value,%2D70%20(minus%2070).
    CONN_POOR = -80
    CONN_OK = -70
    CONN_GOOD = -67
    CONN_EXCELLENT = -30

    CONN_NOT_AVAILABLE_MSG = 'N/A'
    CONN_BAD_MSG = 'Bad'
    CONN_POOR_MSG = 'Poor'
    CONN_OK_MSG = 'Ok'
    CONN_GOOD_MSG = 'Good'
    CONN_EXCELLENT_MSG = 'Excellent'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='gardens', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=_default_garden_name)
    image = models.ImageField(default=_default_garden_image)
    is_connected = models.BooleanField(default=_default_is_connected)
    last_connection_ip = models.GenericIPAddressField(null=True)
    last_connection_time = models.DateTimeField(null=True)
    update_interval = models.DurationField(default=_default_update_interval)
    connection_strength = models.SmallIntegerField(null=True)
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

    def update(self, request: Request):
        self.is_connected = True
        self.last_connection_ip = request.META.get('REMOTE_ADDR')
        self.last_connection_time = datetime.now(pytz.UTC)
        self.save()

    def get_connection_strength_display(self):
        if self.connection_strength is None:
            return self.CONN_NOT_AVAILABLE_MSG
        elif self.connection_strength >= self.CONN_EXCELLENT:
            return self.CONN_EXCELLENT_MSG
        elif self.connection_strength >= self.CONN_GOOD:
            return self.CONN_GOOD_MSG
        elif self.connection_strength >= self.CONN_OK:
            return self.CONN_OK_MSG
        elif self.connection_strength >= self.CONN_POOR:
            return self.CONN_POOR_MSG
        else:
            return self.CONN_BAD_MSG

    def update_interval_display(self):
        total = self.update_interval.total_seconds()
        minutes, seconds = divmod(total, 60)
        minutes = int(minutes)
        seconds = int(seconds)
        string = ''
        if minutes != 0:
            string += f'{minutes} Min '
        if seconds != 0:
            string += f'{seconds} Sec'
        return string.strip()


class Token(models.Model):
    garden = models.OneToOneField(Garden, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)


class WateringStation(models.Model):
    ACTIVE_STATUS_STR = 'Active'
    INACTIVE_STATUS_STR = 'Inactive'

    garden = models.ForeignKey(Garden, related_name='watering_stations', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    moisture_threshold = models.IntegerField(default=_default_moisture_threshold)
    watering_duration = models.DurationField(default=_default_watering_duration)
    plant_type = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=_default_status)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('watering-station-detail', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    def get_update_url(self):
        return reverse('watering-station-update', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

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
