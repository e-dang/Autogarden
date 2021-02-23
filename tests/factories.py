import factory


class GardenFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')

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

    class Meta:
        model = 'garden.WateringStation'
