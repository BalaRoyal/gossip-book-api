from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class UserProfileAdapter(DefaultSocialAccountAdapter):
    """
    Force django all auth to use a custom user model.
    """

    def save_user(self, request, user, form, commit=False):
        return super(UserProfileAdapter, self).save_user(
            request, user, form, commit=True)
