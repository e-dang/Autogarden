from typing import Any

from crispy_forms.utils import render_crispy_form
from django import http
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from garden.forms import (BulkUpdateWateringStationForm, DeleteGardenForm,
                          DeleteWateringStationForm, NewGardenForm,
                          UpdateGardenForm, WateringStationForm)

from .models import Garden, WateringStation
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
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = NewGardenForm()
        gardens = Garden.objects.all()
        return render(request, 'garden_list.html', context={'gardens': gardens, 'form': form})

    def post(self, request: http.HttpRequest) -> http.JsonResponse:
        form = NewGardenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'url': request.build_absolute_uri(reverse('garden-list'))
            })

        form_html = render_crispy_form(form, context=csrf(request))
        return JsonResponse({'success': False, 'html': form_html})


class GardenDetailView(View):
    def get(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        garden = Garden.objects.get(pk=pk)
        return render(request, 'garden_detail.html', context={'garden': garden})


class GardenUpdateView(View):
    def get(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        garden = Garden.objects.get(pk=pk)
        form = UpdateGardenForm(instance=garden)
        return render(request, 'garden_update.html', context={'form': form})

    def post(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        garden = Garden.objects.get(pk=pk)
        form = UpdateGardenForm(request.POST, request.FILES, instance=garden)
        if form.is_valid():
            form.save()
        return redirect('garden-update', pk=pk)


class GardenDeleteView(View):
    def get(self, request: http.HttpRequest, pk: int) -> http.JsonResponse:
        form = DeleteGardenForm()
        form.helper.form_action = reverse('garden-delete', kwargs={'pk': pk})
        form_html = render_crispy_form(form, context=csrf(request))
        return JsonResponse({'html': form_html})

    def post(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        garden = Garden.objects.get(pk=pk)
        garden.delete()
        return redirect('garden-list')


class WateringStationListView(View):
    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        method = request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk) -> http.HttpResponse:
        garden = Garden.objects.get(pk=pk)
        garden.watering_stations.create()
        return redirect('garden-detail', pk=pk)

    def patch(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        garden = Garden.objects.get(pk=pk)
        for station in garden.watering_stations.all():
            form = BulkUpdateWateringStationForm(instance=station, data=request.POST)
            if form.is_valid():
                form.save()
        return redirect('garden-detail', pk=pk)


class WateringStationDetailView(View):
    def get(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.HttpResponse:
        garden = Garden.objects.get(pk=garden_pk)
        station = garden.watering_stations.get(pk=ws_pk)
        form = WateringStationForm(instance=station)
        return render(request, 'watering_station.html', context={'form': form})

    def post(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.JsonResponse:
        garden = Garden.objects.get(pk=garden_pk)
        station = garden.watering_stations.get(pk=ws_pk)
        form = WateringStationForm(instance=station, data=request.POST)
        if form.is_valid():
            form.save()
        form_html = render_crispy_form(form, context=csrf(request))
        return JsonResponse({'html': form_html})


class WateringStationDeleteView(View):
    def get(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.JsonResponse:
        form = DeleteWateringStationForm()
        form.helper.form_action = reverse('watering-station-delete', kwargs={'garden_pk': garden_pk, 'ws_pk': ws_pk})
        form_html = render_crispy_form(form, context=csrf(request))
        return JsonResponse({'html': form_html})

    def post(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.HttpResponse:
        station = WateringStation.objects.get(garden=garden_pk, pk=ws_pk)
        station.delete()
        return redirect('garden-detail', pk=garden_pk)
