from rest_framework import serializers
from .models import Question, QuestionComment
from taggit.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class QuestionCommentSerializer(serializers.ModelSerializer):
    """ Converts question comment model to and from JSON."""

    class Meta:
        model = QuestionComment
        fields = '__all__'

        read_only_fields = ('updated_at', 'created_at')


class QuestionSerializer(serializers.ModelSerializer):
    """Convert question model object to and from JSON."""

    tags = TagSerializer(many=True, read_only=True)
    comments = QuestionCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')
