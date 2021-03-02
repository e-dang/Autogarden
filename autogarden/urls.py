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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from garden.views import (GardenDeleteView, GardenDetailView, GardenListView, GardenUpdateView,
                          GardenAPIView, WateringStationDeleteView, WateringStationDetailView,
                          WateringStationUpdateView, WateringStationListView,
                          WateringStationAPIView)
from users.views import CreateUserView, LoginView, LogoutView

API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),

    path(API_PREFIX + 'garden/<int:pk>/', GardenAPIView.as_view(), name='api-garden'),
    path(API_PREFIX + 'garden/<int:pk>/watering-stations/',
         WateringStationAPIView.as_view(), name='api-watering-stations'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateUserView.as_view(), name='register'),

    path('gardens/', GardenListView.as_view(), name='garden-list'),
    path('gardens/<int:pk>/', GardenDetailView.as_view(), name='garden-detail'),
    path('gardens/<int:pk>/update/', GardenUpdateView.as_view(), name='garden-update'),
    path('gardens/<int:pk>/delete/', GardenDeleteView.as_view(), name='garden-delete'),

    path('gardens/<int:pk>/watering-stations/', WateringStationListView.as_view(), name='watering-station-list'),
    path('gardens/<int:garden_pk>/watering-stations/<int:ws_pk>/',
         WateringStationDetailView.as_view(), name='watering-station-detail'),
    path('gardens/<int:garden_pk>/watering-stations/<int:ws_pk>/update/',
         WateringStationUpdateView.as_view(), name='watering-station-update'),
    path('gardens/<int:garden_pk>/watering-stations/<int:ws_pk>/delete/',
         WateringStationDeleteView.as_view(), name='watering-station-delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
