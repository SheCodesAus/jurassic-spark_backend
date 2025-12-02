from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from rest_framework.authtoken.models import Token


admin.site.register(CustomUser, UserAdmin)
