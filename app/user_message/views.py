from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from .models import Message, Thread
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwner
from rest_framework.response import Response
from django.contrib.auth import get_user_model


class BaseMessageView:
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)


class ListCreateMessageAPIView(BaseMessageView, generics.ListCreateAPIView):
    """
    And endpoint to read user messages.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            receiver = self.kwargs['username']
            thread = Thread.objects.get_or_new(self.request.user, receiver)
            serializer.save(user=self.request.user, thread=thread)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        sender = self.request.user
        thread = Thread.objects.get_or_new(
            sender, self.kwargs['username'])
        return super().get_queryset().filter(thread=thread[0].id)


class MessageDetailAPIView(BaseMessageView, generics.RetrieveUpdateDestroyAPIView):
    """
    An end point to update and or delete as well as retrieve a single
    user message.
    """

    permission_classes = (IsAuthenticated, IsOwner)
