import uuid
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db import models
from django.urls import reverse
from rest_framework.request import Request

from garden.formatters import WateringStationFormatter


def _default_moisture_threshold():
    return 50


def _default_watering_duration():
    return timedelta(minutes=1)


def _default_garden_name():
    return 'My Garden'


def _default_is_connected():
    return False


def _default_update_frequency():
    return timedelta(minutes=5)


def _default_status():
    return True


def _default_garden_image():
    return 'default_garden.png'


class Garden(models.Model):
    OK = 'ok'
    LOW = 'lo'
    WATER_LEVEL_CHOICES = [
        (OK, 'Ok'),
        (LOW, 'Low'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='gardens', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=_default_garden_name)
    image = models.ImageField(default=_default_garden_image)
    is_connected = models.BooleanField(default=_default_is_connected)
    last_connection_ip = models.GenericIPAddressField(null=True)
    last_connection_time = models.DateTimeField(null=True)
    update_frequency = models.DurationField(default=_default_update_frequency)
    connection_strength = models.SmallIntegerField(null=True)
    water_level = models.CharField(choices=WATER_LEVEL_CHOICES, max_length=2, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('garden-detail', kwargs={'pk': self.pk})

    def get_watering_stations_url(self):
        return reverse('watering-station-list', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('garden-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('garden-delete', kwargs={'pk': self.pk})

    def calc_time_till_next_update(self):
        if self.last_connection_time is None:
            return None
        factor = 1
        next_update = self.last_connection_time + factor * self.update_frequency - datetime.now(pytz.UTC)
        while next_update.total_seconds() < 0:
            factor += 1
            next_update = self.last_connection_time + factor * self.update_frequency - datetime.now(pytz.UTC)
        return int(next_update.total_seconds())

    def update_connection_status(self, request: Request):
        self.is_connected = True
        self.last_connection_ip = request.META.get('REMOTE_ADDR')
        self.last_connection_time = datetime.now(pytz.UTC)
        self.save()

    def refresh_connection_status(self):
        if self.last_connection_time is None:
            return

        time_next_update = self.last_connection_time + self.update_frequency - datetime.now(pytz.UTC)
        if time_next_update.total_seconds() < 0:
            self.is_connected = False
            self.connection_strength = None
            self.save()

    def get_watering_station_formatters(self):
        for watering_station in self.watering_stations.all():
            yield WateringStationFormatter(watering_station)

    def get_watering_station_idx(self, watering_station) -> int:
        for i, station in enumerate(self.watering_stations.all()):
            if station == watering_station:
                return i

    def get_watering_station_at_idx(self, idx):
        for i, station in enumerate(self.watering_stations.all()):
            if i == idx:
                return station

    def get_active_watering_stations(self):
        return self.watering_stations.filter(status=True)

    def get_num_active_watering_stations(self):
        return self.get_active_watering_stations().count()

    @property
    def plant_types(self):
        return self.watering_stations.exclude(plant_type__exact='').values_list('plant_type', flat=True)

    @property
    def time_since_last_connection(self):
        if self.last_connection_time is None:
            return None

        return datetime.now(pytz.UTC) - self.last_connection_time


class Token(models.Model):
    garden = models.OneToOneField(Garden, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return str(self.uuid)


class WateringStation(models.Model):
    garden = models.ForeignKey(Garden, related_name='watering_stations', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    moisture_threshold = models.IntegerField(default=_default_moisture_threshold)
    watering_duration = models.DurationField(default=_default_watering_duration)
    plant_type = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=_default_status)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{str(self.garden)} - {self.idx}'

    def get_absolute_url(self):
        return reverse('watering-station-detail', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    def get_update_url(self):
        return reverse('watering-station-update', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    def get_delete_url(self):
        return reverse('watering-station-delete', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    def get_records_url(self):
        return reverse('watering-station-record-list', kwargs={'garden_pk': self.garden.pk, 'ws_pk': self.pk})

    @property
    def idx(self):
        return self.garden.get_watering_station_idx(self)

    def get_formatter(self):
        return WateringStationFormatter(self)


class WateringStationRecord(models.Model):
    watering_station = models.ForeignKey(WateringStation, related_name='records', on_delete=models.CASCADE)
    moisture_level = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.watering_station.garden}/{self.watering_station.idx}/{self.created}'
