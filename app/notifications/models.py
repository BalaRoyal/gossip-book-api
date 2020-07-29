from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Persist user notifications."""

    VOTE = 'VOTE'
    FOLLOW = 'FOLLOW'
    POST = 'POST'
    ANSWER = 'ANSWER'
    COMMENT = 'COMMENT'
    OTHER = 'OTHER'
    MESSAGE = 'MESSAGE'

    ORIGIN_CHOICES = (
        (VOTE, 'post voted'),
        (FOLLOW, 'Profile followed'),
        (ANSWER, 'Question Answered'),
        (COMMENT, 'New post comment'),
        (OTHER, 'Any other notification'),
        (MESSAGE, 'New message')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='notifications')

    message = models.TextField()
    origin = models.CharField(max_length=50, choices=ORIGIN_CHOICES,
                              default=OTHER)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True,
                                      blank=True)
