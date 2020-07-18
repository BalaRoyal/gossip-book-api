from django.db import models
from utils.base_models import BaseGossipQuestionModel

# QUESTION RELATED MODELS


class Question(BaseGossipQuestionModel, models.Model):
    """
    Questions table model.
    ---------------------

    Inherits base question gossip model to get title and timestamp fields
    as well as user.

    """

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.title}"
