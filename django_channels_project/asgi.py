
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

import channels_testing.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_channels_project.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            channels_testing.routing.websocket_urlpatterns
        )
    )
})
