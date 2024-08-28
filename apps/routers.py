from django.urls import path, include


urlpatterns = [
    path('tasks/', include('apps.tasks.urls')),
    path('projects/', include('apps.projects.urls')),
    path('users/', include('apps.users.urls')),
]
