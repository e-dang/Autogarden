from rest_framework import serializers
from .models import Garden, WateringStation

NEGATIVE_NUM_WATERING_STATIONS_ERR = 'Cannot have a negative number of watering stations'


class GardenSerializer(serializers.ModelSerializer):
    num_watering_stations = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Garden
        fields = ['uuid', 'num_watering_stations']

    def validate_num_watering_stations(self, value):
        if value < 0:
            raise serializers.ValidationError(NEGATIVE_NUM_WATERING_STATIONS_ERR)
        return value

    def create(self, validated_data):
        garden = Garden.objects.create(uuid=validated_data['uuid'])
        for _ in range(validated_data['num_watering_stations']):
            garden.watering_stations.create()
        return garden


class WateringStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WateringStation
        fields = ['moisture_threshold', 'watering_duration']