from django.urls import path, include
from . import views

urlpatterns = [
    path('salas/', views.calendar_day, name="calendar_day"),
    path('calendario/<int:id>/', views.calendar_week, name="calendar_week"),
    path('reservar/', views.reserve_room, name="reserve_room"),
    path('moduleconfig/', views.manage_module, name="manage_module"),
    path('moduleid/<int:id>/', views.manage_module_id, name="manage_module_id"),
    path('administrar/solicitudes/', views.manage_request, name="manage_request"),
    path('administrar/solicitudes/<int:id>/', views.manage_request_id, name="manage_request_id"),
    
]