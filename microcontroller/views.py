from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from .serializers import MicroControllerSerializer


class MicroControllerView(APIView):
    def post(self, request):
        serializer = MicroControllerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=HTTP_201_CREATED)
