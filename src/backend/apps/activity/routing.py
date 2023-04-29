from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/activity/enc/<str:enc>", consumers.ChatConsumer.as_asgi())
]