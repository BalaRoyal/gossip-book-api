from django.db import models
from utils.base_models import (BaseGossipQuestionModel,
                               BaseVotesModel,
                               BaseComment)
from django.contrib.auth import get_user_model

from django.dispatch import receiver
from utils.signals import (
    interested_users,
    notify_interested_users,
    comment_signal,
    vote_signal,
    send_post_vote_notification,
    send_comment_notification
)

# Create your models here.


class Gossip(BaseGossipQuestionModel, models.Model):
    """QuestionVoteDetailAPIView
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


@receiver(interested_users, sender=Gossip)
def notify_users(**kwargs):
    notify_interested_users(about='gossip', **kwargs)


@receiver(comment_signal, sender=GossipComment)
def send_cmt_notication(**kwargs):
    """Send comment notification"""

    send_comment_notification('gossip', **kwargs)


@receiver(vote_signal, sender=GossipVote)
def send_qvote_notification(**kwargs):
    """Send question vote notification"""

    send_post_vote_notification('gossip', **kwargs)


@receiver(vote_signal, sender=GossipCommentVote)
def send_qcvote_notification(**kwargs):
    """Send question comment vote notification."""

    send_post_vote_notification('comment', **kwargs)
