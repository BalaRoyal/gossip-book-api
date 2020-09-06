from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailUsernameAuthBackend(ModelBackend):
    """
    Authenticate users with either username or email and password
    """

    def authenticate(self, username=None, password=None):
        """
        Authenticate user base on email address or username if it fails.
        """

        try:
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = get_user_model().objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        """Get user object from the user id."""

        try:
            return get_user_model().objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
