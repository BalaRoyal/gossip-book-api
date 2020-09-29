from django.urls import path

from .views import ListNotificationsAPIView, NotificationDetailsAPIView

urlpatterns = [
    path('notifications/', ListNotificationsAPIView.as_view()),
    path('notifications/<int:pk>', NotificationDetailsAPIView.as_view()),
]
