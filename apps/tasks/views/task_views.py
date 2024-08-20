from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from apps.tasks.models import Task
from apps.tasks.serializers.task_serializers import *


class TaskViewListCreateGenericView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = CreateUpdateTaskSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 15


class TasksListAPIView(APIView):
    paginator = StandardResultsSetPagination

    def get_objects(self) -> QuerySet:
        project_name = self.request.query_params.get('project_name')
        assignee_email = self.request.query_params.get('assignee_email')

        if project_name:
            return Task.objects.filter(project__name=project_name)

        elif assignee_email:
            return Task.objects.filter(assignee__email=assignee_email)

        else:
            return Task.objects.all()

    def get(self, request: Request, *args, **kwargs) -> Response:
        tasks = self.get_objects()

        if not tasks.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        paginator = self.paginator()
        page = paginator.paginate_queryset(tasks, request, view=self)

        if page is not None:
            serializer = AllTasksSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = AllTasksSerializer(tasks, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = CreateUpdateTaskSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TaskDetailAPIView(APIView):
    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['pk'])

    def get(self, request: Request, *args, **kwargs) -> Response:
        task = self.get_object()

        serializer = TaskDetailSerializer(task)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        task = self.get_object()

        serializer = CreateUpdateTaskSerializer(
            instance=task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        task = self.get_object()

        task.delete()

        return Response(
            data={
                "message": "The task has been deleted."
            },
            status=status.HTTP_204_NO_CONTENT
        )

