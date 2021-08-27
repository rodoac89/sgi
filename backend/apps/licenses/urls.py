from django.conf.urls import url, include
"""from django.urls.conf import path
from django.urls.resolvers import URLPattern

from apps.licenses.views import formulario"""
from django.urls import path, include
from .views import adm_licencias, formulario, home, labs, equipos, pc


urlpatterns = [
    path('', home, name = 'index' ),
    path('formulario/', formulario, name = 'formulario'),
    path('labs/', labs, name = 'labs'),
    path('adm_licencias/', adm_licencias, name = 'adm_licencias'),
    path('equipos/', equipos, name = 'equipos'),
    path('pc/', pc, name = 'pc'),
]