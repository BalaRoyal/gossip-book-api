from django.shortcuts import render
from utils.permissions import IsOwner
from .models import (Gossip, GossipComment,
                     GossipVote,
                     GossipCommentVote)

from .serializers import (GossipSerializer,
                          GossipCommentSerializer,
                          GossipVotesSerializer,
                          GossipCommentVotesSerializer)

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)

import rest_framework_filters as filters
from utils.signals import interested_users, comment_signal, vote_signal


class GossipFilter(filters.FilterSet):
    """
    search through questions
    """
    class Meta:
        model = Gossip
        fields = {
            'title':  ['in', 'exact', 'startswith',
                       'endswith', 'contains', 'icontains',
                       'istartswith', 'iexact'],
            'gossip_description':  ['in', 'exact', 'startswith',
                                    'endswith', 'contains', 'icontains',
                                    'istartswith', 'iexact']
        }


class BaseView:
    queryset = Gossip.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = GossipSerializer
    filter_class = GossipFilter
    search_fields = ('title', 'gossip_description')


class BaseCommentView:
    queryset = GossipComment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = GossipCommentSerializer


class BaseGossipVoteView:
    queryset = GossipVote.objects.filter(vote__in=['UPVOTE', 'DOWNVOTE'])
    serializer_class = GossipVotesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class BaseGossipCommentVoteView:
    queryset = GossipCommentVote.objects.filter(
        vote__in=['UPVOTE', 'DOWNVOTE'])

    serializer_class = GossipCommentVotesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ListCreateGossipAPIView(BaseView, viewsets.GenericViewSet,
                              generics.ListCreateAPIView):
    """ 
    Create API endpoints to list and create gossip instances
    """

    name = 'list_gossips'

    def get_queryset(self):

        user = self.request.user
        if not user.is_anonymous:
            interested_topics = user.interested_topics.all()

            queryset = super().get_queryset().filter(tags__in=interested_topics)

            if len(queryset):
                return queryset

        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = None
        tags = None

        if 'tags' in request.data:
            title = request.data['title']
            body = request.data['gossip_description']
            tags = request.data['tags'].split(',')

            serializer = self.get_serializer(
                data={'title': title, 'gossip_description': body})

        else:
            serializer = self.get_serializer(data=request.data)

        if serializer and serializer.is_valid():
            instance = serializer.save(user=request.user)

            if tags:
                instance.tags.add(*tags)

            interested_users.send(sender=Gossip, instance=instance,
                                  user=self.request.user, created=True)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class GossipDetailAPIView(BaseView,
                          generics.RetrieveUpdateDestroyAPIView):
    """
    Creates API endpoints to view a list of all available gossips.
    """

    name = 'gossip_details'

    permission_classes = (IsAuthenticated, IsOwner)


class GossipCommentListCreateAPIView(
        BaseCommentView,
        viewsets.GenericViewSet,
        generics.ListCreateAPIView):
    """
    Create and or list Gossip's comments api endpoints.
    """
    name = 'gossip_comments'

    def get_queryset(self):
        gossip_id = self.kwargs.get('parent_lookup_gossip')
        return super().get_queryset().filter(gossip=gossip_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        gossip_id = self.kwargs.get('parent_lookup_gossip')
        gossip = None

        try:
            gossip = Gossip.objects.get(pk=gossip_id)
        except Gossip.DoesNotExist:
            return Response(data={
                'error': f'The Gossip with ID {gossip_id} Does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            instance = serializer.save(gossip=gossip, user=self.request.user)

            comment_signal.send(sender=GossipComment, post=gossip, instance=instance,
                                user=self.request.user, created=True)

            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class GossipCommentDetailAPIView(
        BaseCommentView,
        viewsets.GenericViewSet,
        generics.RetrieveUpdateDestroyAPIView):
    """
    Update, delete retrieve single Gossip's 
    comment api endpoints.
    """
    name = 'gossip_comment_detail'
    permission_classes = (IsAuthenticated, IsOwner)


class GossipVoteListCreateAPIView(BaseGossipVoteView,
                                  viewsets.GenericViewSet,
                                  generics.ListCreateAPIView):
    """

    """

    def create(self, request, *args, **kwargs):

        vote = request.data['vote']
        gossip_id = self.kwargs.get('parent_lookup_gossip')
        gossip = Gossip.objects.filter(pk=gossip_id).first()

        user = self.request.user

        serializer = self.get_serializer(data={
            'vote': vote,
        })

        # Make sure the user does not vote twice on a single gossip.

        vote_by_user = GossipVote.objects.filter(
            voted_by=self.request.user, gossip=gossip).first()

        if vote_by_user is not None:
            if vote_by_user.vote == vote:
                vote_by_user.vote = 'UNDONE'
            else:
                vote_by_user.vote = vote
                vote_by_user.save()
            return Response(data=self.get_serializer(vote_by_user).data,
                            status=status.HTTP_201_CREATED)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save(voted_by=self.request.user, gossip=gossip)

        # send vote notification

        vote_signal.send(sender=GossipVote, instance=instance, post=gossip,
                         user=self.request.user, created=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class GossipVoteDetailAPIView(BaseGossipVoteView,
                              generics.RetrieveUpdateDestroyAPIView):
    """
    Update and retrieve particular votes API Endpoints.
    """

    permission_classes = (IsAuthenticated, IsOwner)


class CommentVoteListCreateAPIView(BaseGossipCommentVoteView,
                                   viewsets.GenericViewSet,
                                   generics.ListCreateAPIView):
    """
    List gossip comment's votes and vote API endpoints.
    """

    def create(self, request, *args, **kwargs):
        vote = request.data['vote']

        comment_id = self.kwargs.get('parent_lookup_comment')
        comment = GossipComment.objects.filter(pk=comment_id).first()

        user = self.request.user
        serializer = self.get_serializer(data={
            'vote': vote
        })

        vote_by_user = GossipCommentVote.objects.filter(
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

        vote_signal.send(sender=GossipCommentVote, instance=instance, post=comment,
                         user=self.request.user, created=True)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CommentVoteDetailView(BaseGossipCommentVoteView,
                            generics.RetrieveUpdateAPIView):
    """
    Gossip's comment vote detail API endpoints.
    """

    permission_classes = (IsAuthenticated, IsOwner)
