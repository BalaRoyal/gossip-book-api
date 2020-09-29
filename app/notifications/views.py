from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwner

from .models import Notification
from .serializers import NotificationSerializer


class BaseNotificationsView:
    serializer_class = NotificationSerializer
    queryset = Notification.objects.filter(is_read=False)
    permission_classes = (IsAuthenticated,)


class ListNotificationsAPIView(BaseNotificationsView, generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        )


class NotificationDetailsAPIView(BaseNotificationsView,
                                 generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, IsOwner)
