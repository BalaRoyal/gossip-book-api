from rest_framework import serializers
from .models import (Question,
                     QuestionComment,
                     QuestionVote,
                     QuestionCommentVote)
from taggit.models import Tag
from user_profile.serializers import UserSerializer


class QuestioVoteSerializer(serializers.ModelSerializer):
    """
    Convert question votes table model to and form json
    """

    class Meta:
        model = QuestionVote
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'voted_by', 'question')


class QuestionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'id')


class QuestionCommentVoteSerializer(serializers.ModelSerializer):
    """
    Convert question comment votes table model to and from json
    """

    class Meta:
        model = QuestionCommentVote
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'voted_by', 'comment')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class QuestionCommentSerializer(serializers.ModelSerializer):
    """ Converts question comment model to and from JSON."""

    votes = QuestionCommentVoteSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    question = QuestionTitleSerializer(read_only=True)

    class Meta:
        model = QuestionComment
        fields = '__all__'
        read_only_fields = ('updated_at', 'created_at', 'question', 'user')


class QuestionSerializer(serializers.ModelSerializer):
    """Convert question model object to and from JSON."""

    tags = TagSerializer(many=True, read_only=True)
    comments = QuestionCommentSerializer(many=True, read_only=True)
    votes = QuestioVoteSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')
