from django.urls import path, include
from . import views

urlpatterns = [
    path('calendar/day/', views.calendar_day, name="calendar_day"),
    path('calendar/week/<int:id>/', views.calendar_week, name="calendar_week"),
    path('module/', views.manage_module, name="manage_module"),
    path('module/<int:id>/', views.manage_module_id, name="manage_module_id"),
    path('manage/request/', views.manage_request, name="manage_request"),
    path('manage/request/<int:id>/', views.manage_request_id, name="manage_request_id"),
    path('report/', views.report_data, name="report_data"),
    path('reserve/', views.reserve_room, name="reserve_room"),
]