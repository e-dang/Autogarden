from uuid import uuid4

from .models import Garden


def set_num_watering_stations(garden, num_watering_stations):
    difference = num_watering_stations - garden.watering_stations.count()
    for _ in range(difference):
        garden.watering_stations.create()


def create_unique_garden_uuid():
    uuid = uuid4()
    while Garden.objects.filter(uuid=uuid).exists():
        uuid = uuid4()
    return uuid
