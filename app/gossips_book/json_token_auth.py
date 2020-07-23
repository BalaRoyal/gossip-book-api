from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from http import cookies
from asgiref.sync import async_to_sync, sync_to_async


class JsonWebTokenAuthenticationFromScope(BaseJSONWebTokenAuthentication):
    """
    Extracts the JWT from a channel scope (instead of an http request)
    """

    def get_jwt_value(self, scope):
        try:
            cookie = next(x for x in scope['headers'] if x[0].decode(
                'utf-8') == 'cookie')[1].decode('utf-8')
            return cookies.SimpleCookie(cookie)['JWT'].value
        except:
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
            import pdb
            pdb.set_trace()
            scope['user'] = AnonymousUser()

        return self.inner(scope)


def JsonTokenAuthMiddlewareStack(inner):
    return JsonTokenAuthMiddleware(AuthMiddlewareStack(inner))
