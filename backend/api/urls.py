from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import socket

HOSTNAME = ""
try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'

schema_view = get_schema_view(
   openapi.Info(
      title="Labs API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   # url="https://"+HOSTNAME+"/api"
)

urlpatterns = [
    # auth
    path('', include('rest_framework.urls'), name='rest_framework'),
    path('auth/', include('api.authentication.urls')),#include('rest_auth.urls'), name='rest_auth'),
    # Apiviews
    path('core/', include('api.core.urls')),
    # swagger docs
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]