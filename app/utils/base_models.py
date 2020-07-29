from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


class BaseGossipQuestionModel(models.Model):
    """ Creates common fields for questions and gossips model. """

    title = models.TextField()
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.title}"


class BaseComment(models.Model):
    """ Question comments table model. """

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.comment}"

    def __rpr__(self):
        return f"{self.comment} created at {self.created_ats}"


class BaseVotesModel(models.Model):
    """
    Shared fields for question, comments and gossip votes model.
    """

    UPVOTE = 'UPVOTE'
    DOWNVOTE = 'DOWNVOTE'
    UNDONE = 'UNDONE'

    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
        (UNDONE, 'Undone'),
    )

    voted_by = models.ForeignKey(
        get_user_model(), related_name='user_votes',
        on_delete=models.CASCADE)

    vote = models.TextField(
        max_length=50, choices=VOTE_CHOICES, default=UPVOTE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.vote}"
