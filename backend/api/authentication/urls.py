from django.contrib import admin
from django.urls import path, include
from api.authentication.apiviews import Login, Logout

urlpatterns = [
    # Load data
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
]