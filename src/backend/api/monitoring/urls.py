from django.contrib import admin
from django.urls import path, include
from .apiviews import GetTickets

urlpatterns = [
    path("tickets/", GetTickets.as_view(), name="gettickets"),
]