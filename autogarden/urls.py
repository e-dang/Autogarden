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
from users.forms import CustomChangePasswordForm
from django.contrib import admin
from django.urls import path
from garden.views import (GardenDeleteView, GardenDetailView, GardenListView, GardenUpdateView,
                          GardenAPIView, WateringStationCreateView, WateringStationDeleteView, WateringStationDetailView,
                          WateringStationUpdateView, WateringStationListView,
                          WateringStationAPIView, WateringStationRecordListView, home, TokenUpdateView)
from users.views import CreateUserView, LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, SettingsView
from django.contrib.auth import views as auth_views

API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path(API_PREFIX + 'gardens/<str:name>/', GardenAPIView.as_view(), name='api-garden'),
    path(API_PREFIX + 'gardens/<str:name>/watering-stations/',
         WateringStationAPIView.as_view(), name='api-watering-stations'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('reset_password/', PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reset_password_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html',
                                                                   form_class=CustomChangePasswordForm), name='password_change_view'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),
    path('settings/', SettingsView.as_view(), name='settings'),

    path('gardens/', GardenListView.as_view(), name='garden-list'),
    path('gardens/<int:pk>/', GardenDetailView.as_view(), name='garden-detail'),
    path('gardens/<int:pk>/update/', GardenUpdateView.as_view(), name='garden-update'),
    path('gardens/<int:pk>/delete/', GardenDeleteView.as_view(), name='garden-delete'),

    path('gardens/<int:pk>/watering-stations/', WateringStationListView.as_view(), name='watering-station-list'),
    path('gardens/<int:garden_pk>/watering-stations/<int:ws_pk>/',
         WateringStationDetailView.as_view(), name='watering-station-detail'),
    path('gardens/<int:pk>/watering-stations/create/',
         WateringStationCreateView.as_view(), name='watering-station-create'),
    path('gardens/<int:garden_pk>/watering-stations/<int:ws_pk>/update/',
         WateringStationUpdateView.as_view(), name='watering-station-update'),
    path('gardens/<int:garden_pk>/watering-stations/<int:ws_pk>/delete/',
         WateringStationDeleteView.as_view(), name='watering-station-delete'),
    path('gardens/<int:garden_pk>/watering-stations/<int:ws_pk>/records/',
         WateringStationRecordListView.as_view(), name='watering-station-record-list'),

    path('gardens/<int:pk>/token-reset/', TokenUpdateView.as_view(), name='token-reset'),
]
