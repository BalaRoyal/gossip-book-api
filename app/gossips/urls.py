from django.urls import path
from . import views
from utils.routers import NestedRouter


app_name = 'gossip'

router = NestedRouter()

gossips_router = router.register(
    'gossips', views.ListCreateGossipAPIView,
    basename=views.ListCreateGossipAPIView.name)

gossips_router.register(
    'comments',
    views.GossipCommentListCreateAPIView,
    basename=views.GossipCommentListCreateAPIView.name,
    parents_query_lookups=['gossip'])

gossips_router.register(
    'votes', views.GossipVoteListCreateAPIView,
    parents_query_lookups=['gossip'],
    basename='gossip_vote')

comment_router = router.register(
    'comment', views.GossipCommentDetailAPIView,
    basename='gossip_comment')

comment_router.register('votes',
                        views.CommentVoteListCreateAPIView,
                        basename='comment_votes',
                        parents_query_lookups=['comment'])
urlpatterns = [
    path('gossips/<int:pk>', views.GossipDetailAPIView.as_view(),
         name=views.GossipDetailAPIView.name),

    path('comment-vote/<int:pk>', views.GossipVoteDetailAPIView,
         name='gossip_comment_vote'),
    path('trending-gossips/', views.ListTrendingGossipsAPIView.as_view(),
         name='trending_gossips')

]

urlpatterns += router.urls
