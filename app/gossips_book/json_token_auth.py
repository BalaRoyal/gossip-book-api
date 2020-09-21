from http import cookies
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class JsonWebTokenAuthenticationFromScope(BaseJSONWebTokenAuthentication):
    """
    Extracts the JWT from a channel scope (instead of an http request)
    """

    def get_jwt_value(self, scope):
        try:
            token = parse_qs(scope['query_string'].decode('utf8'))['token'][0]
            return token
        except Exception as error:
            return None


class JsonTokenAuthMiddleware(BaseJSONWebTokenAuthentication):
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):

        try:
            # Close old database connections to prevent usage of timed out connections
            close_old_connections()
            user, jwt_value = JsonWebTokenAuthenticationFromScope().authenticate(scope)
            scope['user'] = user
        except Exception as error:
            scope['user'] = AnonymousUser()

        return self.inner(scope)


def JsonTokenAuthMiddlewareStack(inner):
    return JsonTokenAuthMiddleware(AuthMiddlewareStack(inner))
