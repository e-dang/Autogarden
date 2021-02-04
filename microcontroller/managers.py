from django.db import models


class MicroControllerManager(models.Manager):
    def create(self, uuid, num_watering_stations, **kwargs):
        micro_controller = self.model(uuid=uuid, **kwargs)
        micro_controller.save()

        for _ in range(int(num_watering_stations)):
            micro_controller.watering_stations.create()

        return micro_controller
