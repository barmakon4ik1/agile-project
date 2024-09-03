from django.urls import path
from apps.users.views.user_views import (
    UserListGenericView,
    RegisterUserGenericView,
    UserDetailGenericView)


urlpatterns = [
    path('', UserListGenericView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailGenericView.as_view(), name='user-detail'),
    path('register/', RegisterUserGenericView.as_view(), name='user-register'),
]
