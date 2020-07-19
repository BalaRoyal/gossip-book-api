from django.urls import path
from . import views
from utils.routers import NestedRouter

app_name = 'question'

router = NestedRouter()
questions_router = router.register(
    'questions', views.ListQuestionsAPIView,
    basename='questions')


questions_router.register(
    'comments', views.QuestionCommentListCreateAPIView,
    basename=views.QuestionCommentListCreateAPIView.name,
    parents_query_lookups=['question'])

urlpatterns = [
    path('questions/<int:pk>', views.QuestionDetailAPIView.as_view(),
         name=views.QuestionDetailAPIView.name),
    path('comment/<int:pk>', views.QuestionCommentDetailAPIView.as_view(),
         name=views.QuestionCommentDetailAPIView.name)
]


urlpatterns += router.urls
