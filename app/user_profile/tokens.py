from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# Token Generator


class TokenGenerator(PasswordResetTokenGenerator):
    """Generate Email verification token. """

    def _make_hash_value(self, user, timestamp):
        return f"{text_type(user.pk)}{text_type(timestamp)}{text_type(user.is_active)}"


# Token Generator instance
account_activation_token = TokenGenerator()
