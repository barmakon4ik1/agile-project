from django.urls import path
from apps.projects.views.project_views import ProjectsListAPIView, ProjectDetailAPIView

urlpatterns = [
    path('', ProjectsListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
]