import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import chatrooms.routing
from app.middleware import ASGITenantMainMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_celery.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": (django_asgi_app),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chatrooms.routing.websocket_urlpatterns
            )
        )
    )
})
