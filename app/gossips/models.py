from django.db import models
from utils.base_models import (BaseGossipQuestionModel,
                               BaseVotesModel,
                               BaseComment)
from django.contrib.auth import get_user_model

# Create your models here.


class Gossip(BaseGossipQuestionModel, models.Model):
    """
    User Gossips Table model.
    """

    user = models.ForeignKey(
        get_user_model(), related_name='gossips', on_delete=models.CASCADE)
    gossip_description = models.TextField()

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.title}"


class GossipComment(BaseComment, models.Model):
    """
    User Gossip's comment table model.
    """
    gossip = models.ForeignKey(
        Gossip, related_name='comments',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), related_name='gossip',
        on_delete=models.CASCADE)


class GossipVote(BaseVotesModel, models.Model):
    """
    User Gossip votes table model.
    """
    gossip = models.ForeignKey(
        Gossip, related_name='votes',
        on_delete=models.CASCADE)


class GossipCommentVote(BaseVotesModel, models.Model):
    """
    Gossip's comment votes table model.
    """
    comment = models.ForeignKey(
        GossipComment, related_name='votes',
        on_delete=models.CASCADE)
