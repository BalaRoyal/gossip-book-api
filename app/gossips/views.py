from django.shortcuts import render
from utils.permissions import IsOwner
from .models import Gossip
from .serializers import GossipSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class BaseView:
    queryset = Gossip.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = GossipSerializer


class ListCreateGossipAPIView(BaseView, generics.ListCreateAPIView):
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

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GossipDetailAPIView(BaseView,
                          generics.RetrieveUpdateDestroyAPIView):
    """
    Creates API endpoints to view a list of all available questions.
    """

    name = 'gossip_details'

    permission_classes = (IsAuthenticated, IsOwner)
