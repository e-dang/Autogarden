import factory


class GardenFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.Sequence(lambda x: f'Garden{x}')
    is_connected = factory.Sequence(lambda x: x % 2 == 0)

    class Meta:
        model = 'garden.Garden'

    @factory.post_generation
    def watering_stations(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                WateringStationFactory(garden=self)


class WateringStationFactory(factory.django.DjangoModelFactory):
    garden = factory.SubFactory(GardenFactory)
    moisture_threshold = factory.Faker('random_int', min=0, max=100)
    watering_duration = factory.Faker('time_delta')
    plant_type = factory.Sequence(lambda x: f'lettuce{x}')

    class Meta:
        model = 'garden.WateringStation'
