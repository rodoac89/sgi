from django.urls import path
from .apiviews import Get, GetOptions, GetChart, GetCurrent, StartSession, EndSession, Alive

urlpatterns = [
    path("session", Get.as_view(), name="getsessions"),
    path("session/options", GetOptions.as_view(), name="getoptions"),
    path("session/chart", GetChart.as_view(), name="getchart"),
    path("session/state", GetCurrent.as_view(), name="getstate"),    
    path("session/start", StartSession.as_view()),
    path("session/end", EndSession.as_view()),
    path("session/alive", Alive.as_view())
]