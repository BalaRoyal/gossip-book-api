from question.serializers import TagSerializer
from rest_framework import serializers
from .models import Gossip, GossipComment


class GossipCommentSerializer(serializers.ModelSerializer):
    """ Converts question comment model to and from JSON."""

    class Meta:
        model = GossipComment
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at')


class GossipSerializer(serializers.ModelSerializer):
    """ Convert gossip model instances to and from JSON. """

    tags = TagSerializer(many=True, read_only=True)
    comments = GossipCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Gossip
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
