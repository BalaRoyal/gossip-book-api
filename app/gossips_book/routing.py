from channels.routing import ProtocolTypeRouter, URLRouter
import user_message.routing
from .json_token_auth import JsonTokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': JsonTokenAuthMiddlewareStack(
        URLRouter(user_message.routing.websocket_urlpatterns)
    )
})
