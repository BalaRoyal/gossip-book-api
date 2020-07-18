from django.urls import path
from .views import (UserListAPIView, UserDetailAPIView, ConfirmEmailAPIVIew)
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'user'

urlpatterns = [
    path('profile/<int:pk>', UserDetailAPIView.as_view(),
         name=UserDetailAPIView.name),
    path('list/', UserListAPIView.as_view(), name=UserListAPIView.name),
    path('token-auth/', obtain_jwt_token, name='auth_token'),
    path('confirm-email/<str:token>/<str:uidb64>', ConfirmEmailAPIVIew.as_view(),
         name=ConfirmEmailAPIVIew.name),
]
