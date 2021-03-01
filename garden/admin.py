from django.contrib import admin

from .models import Garden, WateringStation


class GardenAdmin(admin.ModelAdmin):
    pass


class WateringStationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Garden, GardenAdmin)
admin.site.register(WateringStation, WateringStationAdmin)
