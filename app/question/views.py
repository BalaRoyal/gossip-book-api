import rest_framework_filters as filters
from rest_framework.response import Response
from utils.permissions import IsOwner
from rest_framework.reverse import reverse
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)
from .serializers import (
    QuestionSerializer,
    QuestionCommentSerializer,
    QuestioVoteSerializer,
    QuestionCommentVoteSerializer)
from .models import(
    Question,
    QuestionComment,
    QuestionVote,
    QuestionCommentVote
)
from rest_framework import status
from rest_framework import generics, viewsets
from django.contrib.auth.models import AnonymousUser
from utils.signals import (interested_users,
                           comment_signal, vote_signal)

from datetime import datetime, timedelta
from django.db.models import Count
# FILTERS


class QuestionFilter(filters.FilterSet):
    """
    search through questions
    """
    class Meta:
        model = Question
        fields = {'title': ['in', 'exact', 'startswith',
                            'endswith', 'contains', 'icontains',
                            'istartswith', 'iexact']}


class BaseView:
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_class = QuestionFilter
    search_fields = ('title',)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class BaseCommentView(viewsets.GenericViewSet):
    queryset = QuestionComment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = QuestionCommentSerializer


class BaseQuestionVoteView:
    queryset = QuestionVote.objects.filter(vote__in=['UPVOTE', 'DOWNVOTE'])
    serializer_class = QuestioVoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class BaseQuestionCommentVoteView:
    queryset = QuestionCommentVote.objects.filter(
        vote__in=['UPVOTE', 'DOWNVOTE'])
    serializer_class = QuestionCommentVoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


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

            interested_users.send(
                sender=Question, instance=instance, user=self.request.user, created=True)

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):

        user = self.request.user
        if not user.is_anonymous:
            interested_topics = user.interested_topics.all()

            queryset = super().get_queryset().filter(tags__in=interested_topics)

            if len(queryset):
                return queryset

        return super().get_queryset()


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
        generics.ListCreateAPIView):
    """
    Create and or list question's comments api endpoints.
    """
    name = 'question_comment'

    def get_queryset(self):
        question_id = self.kwargs.get('parent_lookup_question')
        return super().get_queryset().filter(question=question_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        question_id = self.kwargs.get('parent_lookup_question')
        question = None

        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return Response(data={
                'error': f'The question with {question_id} id does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            instance = serializer.save(
                question=question, user=self.request.user)

            comment_signal.send(sender=QuestionComment, post=question, instance=instance,
                                user=self.request.user, created=True)

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class QuestionCommentDetailAPIView(
        BaseCommentView,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Update, delete retrieve single question's 
    comment api endpoints.
    """
    name = 'question_comment_detail'
    permission_classes = (IsAuthenticated, IsOwner)


# QUESTION VOTE API VIEWS

class QuestionVoteListCreateAPIView(
        BaseQuestionVoteView,
        viewsets.GenericViewSet,
        generics.ListCreateAPIView):
    """
    Vote and view a question's vote api endpoints.
    """

    def create(self, request, *args, **kwargs):

        vote = request.data['vote']
        question_id = self.kwargs.get('parent_lookup_question')
        question = Question.objects.filter(pk=question_id).first()
        user = self.request.user

        serializer = self.get_serializer(data={
            'vote': vote,
        })

        # Make sure the user does not vote twice on a single question.

        vote_by_user = QuestionVote.objects.filter(
            voted_by=self.request.user, question=question).first()

        # import pdb
        # pdb.set_trace()
        if vote_by_user is not None:
            if vote_by_user.vote == vote:
                vote_by_user.vote = 'UNDONE'
            else:
                vote_by_user.vote = vote

            vote_by_user.save()

            return Response(data=self.get_serializer(vote_by_user).data,
                            status=status.HTTP_201_CREATED)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save(
            voted_by=self.request.user, question=question)

        # Send question vote notification

        vote_signal.send(sender=QuestionVote, instance=instance, post=question,
                         user=self.request.user, created=True)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class QuestionVoteDetailAPIView(BaseQuestionVoteView,
                                generics.RetrieveUpdateDestroyAPIView):
    """
    Update and retrieve particular votes API Endpoints.
    """

    permission_classes = (IsAuthenticated, IsOwner)


class CommentVoteListCreateView(BaseQuestionCommentVoteView,
                                viewsets.GenericViewSet,
                                generics.ListCreateAPIView):
    """
    Question comment vote's api endpoints.
    """

    def create(self, request, *args, **kwargs):
        vote = request.data['vote']

        comment_id = self.kwargs.get('parent_lookup_comment')
        comment = QuestionComment.objects.filter(pk=comment_id).first()

        user = self.request.user
        serializer = self.get_serializer(data={
            'vote': vote
        })

        vote_by_user = QuestionCommentVote.objects.filter(
            voted_by=user, comment=comment).first()

        if vote_by_user is not None:
            if vote_by_user.vote == vote:
                vote_by_user.vote = 'UNDONE'

            else:
                vote_by_user.vote = vote

            vote_by_user.save()

            return Response(data=self.get_serializer(vote_by_user).data,
                            status=status.HTTP_201_CREATED)

        serializer.is_valid(raise_exception=True)
        instance = serializer.save(comment=comment, voted_by=self.request.user)

        # send question comment vote notification

        vote_signal.send(sender=QuestionCommentVote, instance=instance, post=comment,
                         user=self.request.user, created=True)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CommentVoteDetailAPIView(
        BaseQuestionCommentVoteView,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Question comment vote's api endpoints.
    """

    permission_classes = (IsAuthenticated, IsOwner)


class ListTrendingQuestionsAPIView(BaseView, generics.ListAPIView):
    """
    List 5 most trending questions based on either comments or votes.
    """

    def get_queryset(self):
        return super().get_queryset().filter(
            created_at__gte=datetime.now() - timedelta(days=7)
        ).annotate(total_comments=Count('comments'),
                   total_votes=Count('votes')).order_by('-total_comments',
                                                        '-total_votes',
                                                        '-created_at')[:5]
