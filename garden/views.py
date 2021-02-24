from django.http.response import JsonResponse
from garden.forms import NewGardenForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

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


class GardenListView(View):
    def get(self, request):
        form = NewGardenForm()
        gardens = Garden.objects.all()
        return render(request, 'gardens.html', context={'gardens': gardens, 'form': form})

    def post(self, request):
        form = NewGardenForm(data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'url': request.build_absolute_uri(reverse('garden-list'))
            })

        form_html = render_crispy_form(form, context=csrf(request))
        return JsonResponse({'success': False, 'html': form_html})
