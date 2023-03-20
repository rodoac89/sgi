from django.urls import path
from .apiviews import Get, StartSession, EndSession, Alive

urlpatterns = [
    path('session', Get.as_view(), name='getsessions'),
    path('session/start', StartSession.as_view()),
    path('session/end', EndSession.as_view()),
    path('session/alive', Alive.as_view())
]