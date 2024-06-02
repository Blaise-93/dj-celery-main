# import routing into our chat project

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chatrooms.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
           chatrooms.routing.websocket_urlpatterns
        )
    )
})