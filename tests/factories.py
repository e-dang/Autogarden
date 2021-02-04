import factory


class MicroControllerFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    num_watering_stations = factory.Faker('random_int', min=0, max=20)

    class Meta:
        model = 'microcontroller.MicroController'


class WateringStationFactory(factory.django.DjangoModelFactory):
    micro_controller = factory.SubFactory(MicroControllerFactory)

    class Meta:
        model = 'microcontroller.WateringStation'
