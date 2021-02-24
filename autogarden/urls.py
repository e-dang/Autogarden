"""autogarden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from garden.views import GardenView, WateringStationView, GardenListView

API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PREFIX + 'garden/', GardenView.as_view(), name='api-garden'),
    path(API_PREFIX + 'garden/<int:pk>/watering-stations/',
         WateringStationView.as_view(), name='api-watering-stations'),
    path('gardens/', GardenListView.as_view(), name='garden-list')
]
