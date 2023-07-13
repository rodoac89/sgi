"""
ASGI config for labsadmin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labsadmin.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
import apps.activity.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labsadmin.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.activity.routing.websocket_urlpatterns
        )
    )
})