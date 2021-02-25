import factory
from garden.models import Garden, WateringStation
import pytz


class GardenFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Sequence(lambda x: f'Garden{x}')
    is_connected = factory.Sequence(lambda x: x % 2 == 0)
    last_connection_ip = factory.Faker('ipv4')
    last_connection_time = factory.Faker('date_time_between', start_date='-20m', end_date='now', tzinfo=pytz.UTC)
    num_missed_updates = factory.Faker('random_int', min=0, max=100)
    water_level = factory.Iterator(Garden.WATER_LEVEL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Garden

    @factory.post_generation
    def watering_stations(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                if kwargs.get('defaults') == True:
                    WateringStation(garden=self).save()
                else:
                    WateringStationFactory(garden=self)


class WateringStationFactory(factory.django.DjangoModelFactory):
    garden = factory.SubFactory(GardenFactory)
    moisture_threshold = factory.Faker('random_int', min=0, max=100)
    plant_type = factory.Sequence(lambda x: f'lettuce{x}')

    class Meta:
        model = WateringStation
