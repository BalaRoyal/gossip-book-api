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


questions_router.register('votes',
                          views.QuestionVoteListCreateAPIView,
                          basename='votes',
                          parents_query_lookups=['question'])

comment_router = router.register(
    'comment', views.QuestionCommentDetailAPIView,
    basename='question_comment')

comment_router.register('votes',
                        views.CommentVoteListCreateView,
                        parents_query_lookups=['comment'],
                        basename='question_comment_vote')

urlpatterns = [
    path('questions/<int:pk>', views.QuestionDetailAPIView.as_view(),
         name=views.QuestionDetailAPIView.name),

    path('question-vote/<int:pk>',
         views.QuestionVoteDetailAPIView.as_view(),
         name='question_vote_detail'),

    path('comment-vote/<int:pk>', views.CommentVoteDetailAPIView.as_view(),
         name='comment_vote'),
    path('trending-questions/', views.ListTrendingQuestionsAPIView.as_view(),
         name='trending_questions')
]


urlpatterns += router.urls
