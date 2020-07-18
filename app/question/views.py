from rest_framework import status
from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from utils.permissions import IsOwner
from rest_framework.response import Response


class BaseView:
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ListQuestionsAPIView(BaseView, generics.ListCreateAPIView):
    """
    Creates API endpoints to view a list of all available questions.
    """

    permission_classes = (IsAuthenticatedOrReadOnly, )

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

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(BaseView,
                            generics.RetrieveUpdateDestroyAPIView):
    """
    Creates API endpoints to view a list of all available questions.
    """

    name = 'question_details'
    permission_classes = (IsAuthenticated, IsOwner)
