from django.urls import path
from apps.tasks.views.tag_views import TagListAPIView, TagDetailAPIView

urlpatterns = [
    path('tags/', TagListAPIView.as_view()),
    path('tags/<int:pk>/', TagDetailAPIView.as_view()),
]