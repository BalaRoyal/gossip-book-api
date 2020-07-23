from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Convert notification model to and from JSON.

    Args:
        serializers (serializer obj): Inherits 
        the model serializer form serializers class]
    """

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at', 'is_read')
