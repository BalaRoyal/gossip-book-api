from question.serializers import TagSerializer
from rest_framework import serializers
from .models import Gossip


class GossipSerializer(serializers.ModelSerializer):
    """ Convert gossip model instances to and from JSON. """

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Gossip
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
