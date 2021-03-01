from datetime import timedelta
from uuid import uuid4

from django.apps import apps


def set_num_watering_stations(garden, num_watering_stations):
    difference = num_watering_stations - garden.watering_stations.count()
    for _ in range(difference):
        garden.watering_stations.create()


def create_unique_garden_uuid():
    Garden = apps.get_model('garden', 'Garden')
    uuid = uuid4()
    while Garden.objects.filter(uuid=uuid).exists():
        uuid = uuid4()
    return uuid


def derive_duration_string(duration):
    minutes, seconds = divmod(duration.total_seconds(), 60)
    return f'{int(minutes):02d}:{int(seconds):02d}'


def build_duration_string(minutes, seconds):
    return derive_duration_string(timedelta(minutes=minutes, seconds=seconds))
