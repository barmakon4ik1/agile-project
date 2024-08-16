from django.urls import path
from apps.tasks.views.tag_views import *
from apps.tasks.views.task_views import *

urlpatterns = [
    path('', TasksListAPIView.as_view()),
    path('<int:pk>/', TaskDetailAPIView.as_view()),
    path('tags/', TagListAPIView.as_view()),
    path('tags/<int:pk>/', TagDetailAPIView.as_view()),
]