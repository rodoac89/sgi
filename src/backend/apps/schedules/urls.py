from django.urls import path, include
from . import views

urlpatterns = [
    path('salas/', views.salas, name="salas"),
    path('calendario/<int:id>/', views.calendario, name="calendario"),
    path('reservar/', views.reservar, name="reservar"),
    path('moduleconfig/', views.moduleconfig, name="moduleconfig"),
    path('administrar/', views.administrar, name="administrar"),
    path('administrarid/<int:id>/', views.administrarid, name="administrarid"),
    path('moduleid/<int:id>/', views.moduleid, name="moduleid"),
]