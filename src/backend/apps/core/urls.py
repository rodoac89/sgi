from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('administration/', views.administration, name="administration"),
    path('installation/', views.wizard, name="wizard"),
    path('view/room/<room>', views.viewroom, name="viewroom"),
]
