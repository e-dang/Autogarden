from datetime import datetime, timedelta
from garden.formatters import GardenFormatter, WateringStationFormatter
from typing import Any

import pytz
from crispy_forms.utils import render_crispy_form
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from garden.forms import (BulkUpdateWateringStationForm, DeleteGardenForm,
                          DeleteWateringStationForm, GardenForm, NewGardenForm,
                          WateringStationForm)
from garden.permissions import TokenPermission

from .models import Garden, WateringStation
from .permissions import TokenPermission
from .serializers import (GardenGetSerializer, GardenPatchSerializer,
                          WateringStationSerializer)


class GardenAPIView(APIView):
    permission_classes = [TokenPermission]

    def get(self, request: Request, pk: int) -> Response:
        garden = Garden.objects.get(pk=pk)
        self.check_object_permissions(request, garden)
        serializer = GardenGetSerializer(instance=garden)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        garden = Garden.objects.get(pk=pk)
        self.check_object_permissions(request, garden)
        serializer = GardenPatchSerializer(data=request.data, instance=garden)
        if serializer.is_valid():
            serializer.save(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WateringStationAPIView(APIView):
    permission_classes = [TokenPermission]

    def get(self, request: Request, pk: int) -> Response:
        garden = Garden.objects.get(pk=pk)
        self.check_object_permissions(request, garden)
        watering_stations = garden.watering_stations.all()
        serializer = WateringStationSerializer(watering_stations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, pk: int) -> Response:
        garden = Garden.objects.get(pk=pk)
        self.check_object_permissions(request, garden)
        for i, station in enumerate(garden.watering_stations.all()):
            station.records.create(**request.data[i])
        return Response({}, status=status.HTTP_201_CREATED)


class GardenListView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = NewGardenForm()
        gardens = request.user.gardens.all()
        return render(request, 'garden_list.html', context={'gardens': gardens, 'form': form})

    def post(self, request: http.HttpRequest) -> http.JsonResponse:
        form = NewGardenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            return JsonResponse({
                'success': True,
                'url': request.build_absolute_uri(reverse('garden-list'))
            })

        form_html = render_crispy_form(form, context=csrf(request))
        return JsonResponse({'success': False, 'html': form_html})


class GardenDetailView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            garden.refresh_connection_status()
            return render(request, 'garden_detail.html', context={'garden': GardenFormatter(garden)})


class GardenUpdateView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            form = GardenForm(instance=garden)
            return render(request, 'garden_update.html', context={'form': form})

    def post(self, request: http.HttpRequest, pk: int) -> http.JsonResponse:
        try:
            garden = request.user.gardens.get(pk=pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            form = GardenForm(request.POST, request.FILES, instance=garden)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'url': garden.get_update_url()})
            form_html = render_crispy_form(form, context=csrf(request))
            return JsonResponse({'success': False, 'html': form_html})


class GardenDeleteView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest, pk: int) -> http.JsonResponse:
        try:
            request.user.gardens.get(pk=pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            form = DeleteGardenForm()
            form.helper.form_action = reverse('garden-delete', kwargs={'pk': pk})
            form_html = render_crispy_form(form, context=csrf(request))
            return JsonResponse({'html': form_html})

    def post(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            garden.delete()
            return redirect('garden-list')


class WateringStationListView(LoginRequiredMixin, View):
    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        method = request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            garden.watering_stations.create()
            return redirect('garden-detail', pk=pk)

    def patch(self, request: http.HttpRequest, pk: int) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=pk)
        except:
            raise Http404()
        else:
            for station in garden.watering_stations.all():
                form = BulkUpdateWateringStationForm(instance=station, data=request.POST)
                if form.is_valid():
                    form.save()
            return redirect('garden-detail', pk=pk)


class WateringStationDetailView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=garden_pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            for i, station in enumerate(garden.watering_stations.all(), start=1):
                if station.pk == ws_pk:
                    return render(request, 'watering_station_detail.html', context={'watering_station': WateringStationFormatter(station), 'idx': i})


class WateringStationUpdateView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=garden_pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            station = garden.watering_stations.get(pk=ws_pk)
            form = WateringStationForm(instance=station)
            return render(request, 'watering_station_update.html', context={'form': form})

    def post(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.JsonResponse:
        try:
            garden = request.user.gardens.get(pk=garden_pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            station = garden.watering_stations.get(pk=ws_pk)
            form = WateringStationForm(request.POST, request.FILES, instance=station)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'url': station.get_update_url()})
            form_html = render_crispy_form(form, context=csrf(request))
            return JsonResponse({'success': False, 'html': form_html})


class WateringStationDeleteView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.JsonResponse:
        try:
            request.user.gardens.get(pk=garden_pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            form = DeleteWateringStationForm()
            form.helper.form_action = reverse('watering-station-delete',
                                              kwargs={'garden_pk': garden_pk, 'ws_pk': ws_pk})
            form_html = render_crispy_form(form, context=csrf(request))
            return JsonResponse({'html': form_html})

    def post(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.HttpResponse:
        try:
            garden = request.user.gardens.get(pk=garden_pk)
        except Garden.DoesNotExist:
            raise Http404()
        else:
            station = garden.watering_stations.get(garden=garden_pk, pk=ws_pk)
            station.delete()
            return redirect('garden-detail', pk=garden_pk)


class WateringStationRecordListView(LoginRequiredMixin, View):
    def get(self, request: http.HttpRequest, garden_pk: int, ws_pk: int) -> http.JsonResponse:
        try:
            garden = request.user.gardens.get(pk=garden_pk)
            watering_station = garden.watering_stations.get(pk=ws_pk)
        except (Garden.DoesNotExist, WateringStation.DoesNotExist):
            raise Http404()
        else:
            labels = []
            data = []
            cut_off_time = datetime.now(pytz.UTC) - timedelta(hours=12)
            for record in watering_station.records.filter(created__gte=cut_off_time).order_by('created'):
                labels.append(record.created)
                data.append(record.moisture_level)
            return JsonResponse({
                'labels': labels,
                'data': data
            })
