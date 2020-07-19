from django.urls import path
from .views import (UserListAPIView,
                    UserDetailAPIView,
                    ListFollowersAPIView,
                    ListFollowingAPIView,
                    FollowersDetailView,
                    ConfirmEmailAPIVIew)

from rest_framework_jwt.views import obtain_jwt_token
from utils.routers import NestedRouter

app_name = 'user'

router = NestedRouter()

user_detail_router = router.register('profile', UserDetailAPIView)
user_detail_router.register('followers', ListFollowersAPIView,
                            basename='followers', parents_query_lookups=['user'])

user_detail_router.register('following', ListFollowingAPIView,
                            basename='following', parents_query_lookups=['follower'])

user_detail_router.register(
    'unfollow', FollowersDetailView,
    basename='unfollow',
    parents_query_lookups=['user'])

urlpatterns = [
    path(
        'list/', UserListAPIView.as_view({'get': 'list'}), name=UserListAPIView.name),
    path('token-auth/', obtain_jwt_token, name='auth_token'),
    path('confirm-email/<str:token>/<str:uidb64>', ConfirmEmailAPIVIew,
         name=ConfirmEmailAPIVIew.name),
]

urlpatterns += router.urls
