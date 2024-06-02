import os
import chatrooms.routing
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from dotenv import load_dotenv
load_dotenv()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_celery.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # We will add WebSocket protocol later. For now, it's just HTTP.
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chatrooms.routing.websocket_urlpatterns))
        )

    }
)


# application = get_asgi_application()
