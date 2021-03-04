from django.apps import AppConfig


class GardenConfig(AppConfig):
    name = 'garden'

    def ready(self):
        import garden.signals
