from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Garden
from .serializers import GardenSerializer, WateringStationSerializer


class GardenView(APIView):
    def post(self, request):
        try:
            garden = Garden.objects.get(uuid=request.data['uuid'])
        except Garden.DoesNotExist:
            serializer = GardenSerializer(data=request.data)
            if serializer.is_valid():
                garden = serializer.save()
            return Response({'pk': garden.pk}, status=status.HTTP_201_CREATED)
        else:
            return Response({'pk': garden.pk}, status=status.HTTP_409_CONFLICT)


class WateringStationView(APIView):
    def get(self, request, pk):
        garden = Garden.objects.get(pk=pk)
        watering_stations = garden.watering_stations.all()
        serializer = WateringStationSerializer(watering_stations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
