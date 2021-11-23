from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('administration/', views.administration, name="administration"),
    path('load/<dato>', views.load, name="load"),
]
