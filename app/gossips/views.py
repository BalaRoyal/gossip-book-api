from django.shortcuts import render
from utils.permissions import IsOwner
from .models import Gossip, GossipComment
from .serializers import (GossipSerializer,
                          GossipCommentSerializer)
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
        generics.RetrieveUpdateDestroyAPIView):
    """
    Update, delete retrieve single Gossip's 
    comment api endpoints.
    """
    name = 'gossip_comment_detail'
    permission_classes = (IsAuthenticated, IsOwner)
