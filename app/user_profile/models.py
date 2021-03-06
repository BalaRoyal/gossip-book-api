from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.dispatch import receiver
from taggit.managers import TaggableManager
from utils.functions import profile_image_upload_path
from utils.signals import follow_user_signal, send_follow_user_notification


class UserManager(BaseUserManager):
    """ A class to provide helper functions for managing user model. """

    def create_user(self, email, password=None, **kwargs):
        """Create normal user """

        if not email:
            raise ValueError('User should have an email address')

        if not password:
            raise ValueError('User should have a password')

        user = self.model(email=self.normalize_email(
            email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        """ Create super user. """

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User table model """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    interested_topics = TaggableManager()
    profile_image_url = models.ImageField(
        null=True, upload_to=profile_image_upload_path)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # add user interested topics

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserLocation(models.Model):
    """
    User address model.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='address')

    location = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.location}"


class FollowersModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(following=True)


class Followers(models.Model):
    """
    User followers model
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='followers', on_delete=models.CASCADE)

    follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='following', on_delete=models.CASCADE)

    following = models.BooleanField(default=True)

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True, null=True, blank=True)

    # objects = FollowersModelManager()


@receiver(follow_user_signal, sender=Followers)
def send_follow_profile_notification(**kwargs):
    """Send notification when a user starts following another.
    """
    send_follow_user_notification(**kwargs)
