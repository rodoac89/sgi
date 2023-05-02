from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="activity"),
    path('state/', views.state, name="current_state"),
]