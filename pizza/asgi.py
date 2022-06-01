"""
ASGI config for pizza project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import imp
import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from home.consumers import OrderProgress

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza.settings')

application = get_asgi_application()

ws_pattern = [
    path('ws/pizza/<order_id>', OrderProgress),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter(ws_pattern))
})