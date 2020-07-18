from django.db import models
from utils.base_models import BaseGossipQuestionModel

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
