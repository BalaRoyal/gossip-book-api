from django.urls import path
from .consumers import QuestionConsumer

websocket_urlpatterns = [
    path('ws/question/<str:question>', QuestionConsumer)
]
