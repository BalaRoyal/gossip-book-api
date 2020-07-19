from django.urls import path
from . import views

app_name = 'gossip'

urlpatterns = [
    path('gossips/', views.ListCreateGossipAPIView.as_view(),
         name=views.ListCreateGossipAPIView.name),
    path('<int:pk>', views.GossipDetailAPIView.as_view(),
         name=views.GossipDetailAPIView.name),
]
