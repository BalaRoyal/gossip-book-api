from django.db import models
from utils.base_models import (BaseGossipQuestionModel,
                               BaseComment)
from django.contrib.auth import get_user_model

# Create your models here.


class Gossip(BaseGossipQuestionModel, models.Model):
    """
    User Gossips Table model.
    """

    gossip_description = models.TextField()

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.title}"


class GossipComment(BaseComment, models.Model):
    gossip = models.ForeignKey(
        Gossip, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), related_name='gossip',
        on_delete=models.CASCADE)
