from rest_framework.serializers import ModelSerializer
from .models import Message
from django.contrib.auth import get_user_model


class UserSerializer(ModelSerializer):
    """User object model serializer

    Args:
        ModelSerializer (Object): restframework model serializer.
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class MessageSerializer(ModelSerializer):
    """Converts message object to and from JSON.

    Args:
        ModelSerializer (Object): Model object serializer
    """

    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'thread')
