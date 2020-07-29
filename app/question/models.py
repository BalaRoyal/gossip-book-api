from django.db import models
from utils.base_models import (BaseGossipQuestionModel,
                               BaseComment, BaseVotesModel)
from django.contrib.auth import get_user_model

from django.dispatch import receiver

from utils.signals import (
    interested_users,
    notify_interested_users,
    comment_signal,
    send_comment_notification,
    vote_signal,
    send_post_vote_notification
)

# QUESTION RELATED MODELS


class Question(BaseGossipQuestionModel, models.Model):
    """
    Questions table model.
    ---------------------

    Inherits base question gossip model to get title and timestamp fields
    as well as user.

    """
    user = models.ForeignKey(
        get_user_model(), related_name='questions',
        on_delete=models.CASCADE)


class QuestionComment(BaseComment, models.Model):
    """
    Question comment table model
    """
    question = models.ForeignKey(
        Question, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), related_name='comments',
        on_delete=models.CASCADE)


class QuestionVote(BaseVotesModel, models.Model):
    """
    Question upvotes and downvotes model.
    """
    question = models.ForeignKey(
        Question, related_name='votes',
        on_delete=models.CASCADE)


class QuestionCommentVote(BaseVotesModel, models.Model):
    """
    Question comment upvotes and downvotes model.
    """

    comment = models.ForeignKey(
        QuestionComment, related_name='votes',
        on_delete=models.CASCADE)


# Notify interested users when a new quesiton is asked.

@receiver(interested_users, sender=Question)
def notify_users(**kwargs):
    """
    Send notifications to interested users on new question creation.
    """
    notify_interested_users(about='question', **kwargs)


# Notify user of a comment on theri question
@receiver(comment_signal, sender=QuestionComment)
def send_cmt_notication(**kwargs):
    """Send comment notification"""
    send_comment_notification('question', **kwargs)


# Send question vote notification
@receiver(vote_signal, sender=QuestionVote)
def send_qvote_notification(**kwargs):
    """Send question vote notification"""
    send_post_vote_notification('question', **kwargs)


# Send question comment vote notification
@receiver(vote_signal, sender=QuestionCommentVote)
def send_qcvote_notification(**kwargs):
    """Send question comment vote notification."""
    send_post_vote_notification('comment', **kwargs)
