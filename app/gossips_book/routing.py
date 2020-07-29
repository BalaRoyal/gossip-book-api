from channels.routing import ProtocolTypeRouter, URLRouter
import user_message.routing
from .json_token_auth import JsonTokenAuthMiddlewareStack
import notifications.routing

routes = []

routes += user_message.routing.websocket_urlpatterns
routes += notifications.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': JsonTokenAuthMiddlewareStack(
        URLRouter(routes)
    )
})
