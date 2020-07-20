from django.db import models
from utils.base_models import (BaseGossipQuestionModel,
                               BaseComment, BaseVotesModel)
from django.contrib.auth import get_user_model

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
