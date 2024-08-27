from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


urlpatterns = [
    path('', lambda req: HttpResponse("Welcome to my site!")),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.routers')),
]