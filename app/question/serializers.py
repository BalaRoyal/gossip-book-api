from rest_framework import serializers
from .models import Question
from taggit.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Convert question model object to and from JSON."""

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')
