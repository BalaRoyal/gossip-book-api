

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', admin.site.urls),
    path('api/user/', include('user_profile.urls')),
    path('api/question/', include('question.urls')),
    path('api/gossip/', include('gossips.urls')),
    path('api/user-message/', include('user_message.urls')),
]
