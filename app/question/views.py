from rest_framework import status
from rest_framework import generics, viewsets
from .models import Question, QuestionComment
from .serializers import (QuestionSerializer,
                          QuestionCommentSerializer)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)
from rest_framework.reverse import reverse
from utils.permissions import IsOwner
from rest_framework.response import Response


class BaseView:
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class BaseCommentView:
    queryset = QuestionComment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QuestionCommentSerializer


class ListQuestionsAPIView(BaseView, viewsets.GenericViewSet,
                           generics.ListCreateAPIView):
    """
    Creates API endpoints to view a list of all 
    available questions.17:30, no
    """

    name = 'list_questions'

    def create(self, request, *args, **kwargs):
        serializer = None
        tags = None

        if 'tags' in request.data:
            question = request.data['title']
            tags = request.data['tags'].split(',')

            serializer = self.get_serializer(data={'title': question})

        else:
            serializer = self.get_serializer(data=request.data)

        if serializer and serializer.is_valid():
            instance = serializer.save(user=request.user)

            if tags:
                instance.tags.add(*tags)

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(
        BaseView,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Creates API endpoints to view a list of all 
    available questions.
    """

    name = 'question_details'
    permission_classes = (IsAuthenticated, IsOwner)


class QuestionCommentListCreateAPIView(
        BaseCommentView,
        viewsets.GenericViewSet,
        generics.ListCreateAPIView):
    """
    Create and or list question's comments api endpoints.
    """
    name = 'question_comment'


class QuestionCommentDetailAPIView(
        BaseCommentView,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Update, delete retrieve single question's 
    comment api endpoints.
    """
    name = 'question_comment_detail'
    permission_classes = (IsAuthenticated, IsOwner)
