from django.urls import path
from apps.users.views.user_views import UserListGenericView


urlpatterns = [
    path('', UserListGenericView.as_view()),
]