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

urlpatterns = [
    path('gossips/<int:pk>', views.GossipDetailAPIView.as_view(),
         name=views.GossipDetailAPIView.name),

    path('comment/<int:pk>', views.GossipCommentDetailAPIView.as_view(),
         name=views.GossipCommentDetailAPIView.name)

]

urlpatterns += router.urls
