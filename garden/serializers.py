from rest_framework import serializers
from rest_framework.request import Request

from .models import Garden, WateringStation


class GardenGetSerializer(serializers.ModelSerializer):
    update_interval = serializers.SerializerMethodField()

    class Meta:
        model = Garden
        fields = ['update_interval']

    def get_update_interval(self, obj):
        return obj.update_interval.total_seconds()


class GardenPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ['water_level', 'connection_strength']
        extra_kwargs = {
            'water_level': {'required': True},
            'connection_strength': {'required': True}
        }

    def save(self, request: Request, **kwargs):
        self.instance.update(request)
        return super().save(**kwargs)


class WateringStationSerializer(serializers.ModelSerializer):
    watering_duration = serializers.SerializerMethodField()

    class Meta:
        model = WateringStation
        fields = ['status', 'moisture_threshold', 'watering_duration']

    def get_watering_duration(self, obj):
        return obj.watering_duration.total_seconds()
