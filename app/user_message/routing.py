from django.urls import path
from .consumers import MessageConsumer

websocket_urlpatterns = [
    path('ws/message/<str:username>', MessageConsumer)
]
