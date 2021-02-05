from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import MicroController
from .serializers import MicroControllerSerializer, WateringStationSerializer


class MicroControllerView(APIView):
    def post(self, request):
        try:
            micro_controller = MicroController.objects.get(uuid=request.POST['uuid'])
        except MicroController.DoesNotExist:
            serializer = MicroControllerSerializer(data=request.data)
            if serializer.is_valid():
                micro_controller = serializer.save()
            return Response({'pk': micro_controller.pk}, status=status.HTTP_201_CREATED)
        else:
            return Response({'pk': micro_controller.pk}, status=status.HTTP_409_CONFLICT)


class WateringStationView(APIView):
    def get(self, request, pk):
        micro_controller = MicroController.objects.get(pk=pk)
        watering_stations = micro_controller.watering_stations.all()
        serializer = WateringStationSerializer(watering_stations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
