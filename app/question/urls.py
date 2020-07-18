from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('questions/', views.ListQuestionsAPIView.as_view(),
         name=views.ListQuestionsAPIView.name),
    path('<int:pk>', views.QuestionDetailAPIView.as_view(),
         name=views.QuestionDetailAPIView.name),
]
