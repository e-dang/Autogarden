from django import http
from django.shortcuts import redirect, render
from django.views import View
from users.forms import UserCreateForm, LoginForm
from django.contrib.auth import login, logout


class LoginView(View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        form = LoginForm()
        return render(request, 'login.html', context={'form': form})

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():  # form calls authenticate
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('garden-list')
        return render(request, 'login.html', context={'form': form})


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
