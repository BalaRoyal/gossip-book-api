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


class BaseView:
    queryset = Gossip.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = GossipSerializer


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

        # Make sure the user does not vote twice on a single question.

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

        serializer.save(voted_by=self.request.user, gossip=gossip)

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
        serializer.save(comment=comment, voted_by=self.request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CommentVoteDetailView(BaseGossipCommentVoteView,
                            generics.RetrieveUpdateAPIView):
    """
    Gossip's comment vote detail API endpoints.
    """

    permission_classes = (IsAuthenticated, IsOwner)
