from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from apps.users.models import User
from apps.users.serializers.user_serializers import UserListSerializer, RegisterUserSerializer


class UserListGenericView(ListAPIView):
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

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class RegisterUserGenericView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
