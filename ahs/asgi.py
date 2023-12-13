"""
ASGI config for AHS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path

from core.consumer import TerminalWorker, CoreConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahs.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,

    'channel': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            ChannelNameRouter({
                'test': CoreConsumer.as_asgi(),
            })
        )
    ),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter({
                re_path(r"ws/(?P<room_name>\w+)/$", TerminalWorker.as_asgi()),
            })
        )
    ),
})
