from django import http
from django.contrib.auth import login, logout, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from users.forms import (CustomPasswordResetForm, CustomSetPasswordForm,
                         LoginForm, UpdateUserForm, UserCreateForm)


class LoginView(DefaultLoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class LogoutView(View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        logout(request)
        return redirect('login')


class CreateUserView(View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = UserCreateForm()
        return render(request, 'register.html', context={'form': form})

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('garden-list')
        return render(request, 'register.html', context={'form': form})


class PasswordResetView(views.PasswordResetView):
    form_class = CustomPasswordResetForm


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


class SettingsView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = UpdateUserForm(instance=request.user)
        return render(request, 'settings.html', context={'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UpdateUserForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, 'settings.html', context={'form': form})
