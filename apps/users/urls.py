from django.urls import path
from apps.users.views.user_views import *


urlpatterns = [
    path('register/', RegisterUserGenericView.as_view(), name='register'),
]
