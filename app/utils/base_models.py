from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


class BaseGossipQuestionModel(models.Model):
    """ Creates common fields for questions and gossips model. """

    user = models.ForeignKey(
        get_user_model(), related_name='questions',
        on_delete=models.CASCADE)

    title = models.TextField()
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
