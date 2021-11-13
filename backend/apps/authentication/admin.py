from django.contrib import admin
from django.contrib import admin
from apps.authentication.models import Role, UserProfile

admin.site.register(Role)
admin.site.register(UserProfile)
