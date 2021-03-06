from rest_framework import serializers

from question.serializers import TagSerializer
from user_profile.serializers import UserSerializer

from .models import Gossip, GossipComment, GossipCommentVote, GossipVote


class GossipTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gossip
        fields = ('title', 'id')


class GossipVotesSerializer(serializers.ModelSerializer):
    """
    convert gossip votes model to and from json.
    """

    class Meta:
        model = GossipVote
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'gossip', 'voted_by')


class GossipCommentVotesSerializer(serializers.ModelSerializer):
    """
    convert gossip votes model to and from json.
    """

    gossip = GossipTitleSerializer(read_only=True)

    class Meta:
        model = GossipCommentVote
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'comment', 'voted_by')


class GossipCommentSerializer(serializers.ModelSerializer):
    """ Converts question comment model to and from JSON."""

    votes = GossipCommentVotesSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = GossipComment
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at', 'user', 'gossip')


class GossipSerializer(serializers.ModelSerializer):
    """ Convert gossip model instances to and from JSON. """

    tags = TagSerializer(many=True, read_only=True)
    comments = GossipCommentSerializer(many=True, read_only=True)
    votes = GossipVotesSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Gossip
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')
