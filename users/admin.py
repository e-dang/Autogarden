from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = [field for field in BaseUserAdmin.ordering if field != 'username']


admin.site.register(User, UserAdmin)
