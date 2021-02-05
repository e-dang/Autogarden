import factory


class MicroControllerFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')

    class Meta:
        model = 'microcontroller.MicroController'

    @factory.post_generation
    def watering_stations(self, create, count, **kwargs):
        if not create:
            return

        if count:
            for _ in range(count):
                WateringStationFactory(micro_controller=self)


class WateringStationFactory(factory.django.DjangoModelFactory):
    micro_controller = factory.SubFactory(MicroControllerFactory)

    class Meta:
        model = 'microcontroller.WateringStation'
