from datetime import timedelta
from functools import partial
from garden.serializers import GardenPatchSerializer
from garden.utils import derive_duration_string
from typing import Any, Dict

import factory
import pytz
from django.db.models.signals import post_save
from factory import Factory
from factory.base import StubObject
from garden.models import Garden, Token, WateringStation, WateringStationRecord
from users.models import User

TEST_PASSWORD = 'test-password123'


def random_valid_duration(min_seconds, max_seconds):
    seconds_diff = max_seconds - min_seconds
    rand_time_delta = factory.Faker('time_delta', end_datetime=timedelta(
        seconds=seconds_diff)).evaluate('', '', {'locale': None})
    return rand_time_delta + timedelta(seconds=min_seconds)


def generate_dict_factory(factory: Factory):
    """https://github.com/FactoryBoy/factory_boy/issues/68"""

    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)


class JsonFactoryMixin:
    @classmethod
    def json(cls, **kwargs):
        return generate_dict_factory(cls)(**kwargs)

    @classmethod
    def json_subset(cls, keys, **kwargs):
        data = cls.json(**kwargs)
        return {key: data[key] for key in keys}

    @classmethod
    def json_batch(cls, num, **kwargs):
        factory = generate_dict_factory(cls)
        return [factory(**kwargs) for _ in range(num)]


class UserFactory(factory.django.DjangoModelFactory, JsonFactoryMixin):
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

    @classmethod
    def signup_info(cls, **kwargs):
        keys = ['email', 'first_name', 'last_name', 'password']
        data = super().json_subset(keys, **kwargs)
        data['password1'] = data['password']
        data['password2'] = data['password']
        data.pop('password')
        return data


@factory.django.mute_signals(post_save)
class TokenFactory(factory.django.DjangoModelFactory, JsonFactoryMixin):
    garden = factory.SubFactory('tests.factories.GardenFactory', token=None)
    uuid = factory.Faker('uuid4')

    class Meta:
        model = Token


@factory.django.mute_signals(post_save)
class GardenFactory(factory.django.DjangoModelFactory, JsonFactoryMixin):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda x: f'Garden{x}')
    token = factory.RelatedFactory(TokenFactory, factory_related_name='garden')
    is_connected = factory.Sequence(lambda x: x % 2 == 0)
    last_connection_ip = factory.Faker('ipv4')
    last_connection_time = factory.Faker('date_time_between', start_date='-20m', end_date='now', tzinfo=pytz.UTC)
    water_level = factory.Iterator(Garden.WATER_LEVEL_CHOICES, getter=lambda c: c[0])
    connection_strength = factory.Faker('random_int', min=-100, max=0)
    update_frequency = factory.LazyFunction(lambda: random_valid_duration(1, 60))

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

    @classmethod
    def form_fields(cls, **kwargs):
        keys = ['name', 'update_frequency']
        return super().json_subset(keys, **kwargs)

    @classmethod
    def patch_serializer_fields(cls, **kwargs):
        keys = GardenPatchSerializer.Meta.fields
        return super().json_subset(keys, **kwargs)


class WateringStationFactory(factory.django.DjangoModelFactory, JsonFactoryMixin):
    garden = factory.SubFactory(GardenFactory)
    moisture_threshold = factory.Faker('random_int', min=0, max=100)
    plant_type = factory.Sequence(lambda x: f'lettuce{x}')
    status = factory.Sequence(lambda x: x % 2 == 0)
    watering_duration = factory.LazyFunction(lambda: random_valid_duration(1, 20))

    class Meta:
        model = WateringStation

    @factory.post_generation
    def records(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                WateringStationRecordFactory(garden=self)

    @classmethod
    def form_fields(cls, **kwargs):
        keys = ['moisture_threshold', 'watering_duration', 'plant_type', 'status']
        data = super().json()
        form_data = {key: data[key] for key in keys}
        form_data['watering_duration'] = derive_duration_string(form_data['watering_duration'])
        return form_data


class WateringStationRecordFactory(factory.django.DjangoModelFactory, JsonFactoryMixin):
    watering_station = factory.SubFactory(WateringStationFactory)
    moisture_level = factory.Faker('random_int', min=0, max=100)

    class Meta:
        model = WateringStationRecord
