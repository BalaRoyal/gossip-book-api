from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from utils.routers import NestedRouter

from .views import (ConfirmEmailAPIVIew, FacebookLoginView,
                    FollowersDetailView, GoogleLoginView, InitConfigView,
                    ListFollowersAPIView, ListFollowingAPIView, ListUserAnswer,
                    ListUserGossipComments, UserDetailAPIView,
                    UserInterestedTopicsAPIView,
                    UserInterestedTopicsListAPIView, UserListAPIView)

app_name = 'user'

router = NestedRouter()

# BASE PROFILE URL
user_detail_router = router.register('profile', UserDetailAPIView)

# USER PROFILE FOLLOWERS
user_detail_router.register('followers', ListFollowersAPIView,
                            basename='followers', parents_query_lookups=['user'])

# USERS FOLLOWED BY USER PROFILE
user_detail_router.register('following', ListFollowingAPIView,
                            basename='following', parents_query_lookups=['follower'])

urlpatterns = [
    path('all/', UserListAPIView.as_view({'get': 'list'}),
         name=UserListAPIView.name),

    path('confirm-email/<str:token>/<str:uidb64>', ConfirmEmailAPIVIew,
         name=ConfirmEmailAPIVIew.name),

    path('interested-topics', UserInterestedTopicsListAPIView.as_view({
        'get': 'list'
    }),
        name='interested_topics'),
    path('interested-topics<int:pk>', UserInterestedTopicsAPIView.as_view()),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('auth/facebook/', FacebookLoginView.as_view(), name='fb_login'),
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('init-admin/', InitConfigView.as_view(), name='init_admin'),
    path('answers/', ListUserAnswer.as_view()),
    path('comments/', ListUserGossipComments.as_view()),
]

urlpatterns += router.urls
