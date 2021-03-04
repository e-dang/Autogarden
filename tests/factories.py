import factory
import pytz
from django.db.models.signals import post_save
from garden.models import Garden, Token, WateringStation, WateringStationRecord
from users.models import User

TEST_PASSWORD = 'test-password123'


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('ascii_email')

    class Meta:
        model = User

    @factory.post_generation
    def gardens(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                GardenFactory(owner=self)


@factory.django.mute_signals(post_save)
class TokenFactory(factory.django.DjangoModelFactory):
    garden = factory.SubFactory('tests.factories.GardenFactory', profile=None)
    uuid = factory.Faker('uuid4')

    class Meta:
        model = Token


@factory.django.mute_signals(post_save)
class GardenFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: f'Garden{x}')
    token = factory.RelatedFactory(TokenFactory, factory_related_name='garden')
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
    status = factory.Sequence(lambda x: x % 2 == 0)

    class Meta:
        model = WateringStation

    @factory.post_generation
    def records(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                WateringStationRecordFactory(garden=self)


class WateringStationRecordFactory(factory.django.DjangoModelFactory):
    garden = factory.SubFactory(WateringStationFactory)
    moisture_level = factory.Faker('random_int', min=0, max=100)

    class Meta:
        model = WateringStationRecord
