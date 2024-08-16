from django.urls import path
from apps.projects.views.project_views import *
from apps.projects.views.project_file_views import *

urlpatterns = [
    path('', ProjectsListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
    path('files/', ProjectFileListAPIView.as_view()),
]