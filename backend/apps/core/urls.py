from django.urls import path, include
from . import views

urlpatterns = [
    path('saludo/', views.saludo, name="saludo"),
    path('', views.index, name="index"),
    
]