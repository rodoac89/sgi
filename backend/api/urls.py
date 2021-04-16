from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
)

urlpatterns = [
    # auth
    path('', include('rest_framework.urls'), name='rest_framework'),
    path('auth/', include('api.authentication.urls')),#include('rest_auth.urls'), name='rest_auth'),
    # Apiviews
    path('core/', include('api.core.urls')),
    # swagger docs
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')

]