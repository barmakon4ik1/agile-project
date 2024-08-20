from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from apps.users.models import User
from apps.users.serializers.user_serializers import UserListSerializer


class UserListGenericView(ListAPIView): # (ListCreateAPIView) - поменяет вид формы на вместе со созданием
    serializer_class = UserListSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get('project_name')
        if project_name:
            return User.objects.filter(project__name=project_name)
        return User.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        projects = self.get_queryset()
        if not projects.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)