from django.urls import path
from . import views

urlpatterns = [
    path('messages/<str:username>',
         views.ListCreateMessageAPIView.as_view(),
         name='thread_message'),
    path('message/<int:pk>',
         views.MessageDetailAPIView.as_view(),
         name='message_detail')
]
