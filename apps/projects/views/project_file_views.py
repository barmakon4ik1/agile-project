from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveDestroyAPIView
from apps.projects.models import ProjectFile, Project
from apps.projects.serializers.project_file_serializers import *


class ProjectFileListGenericView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AllProjectFilesSerializer
        return CreateProjectFileSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get('project')

        if project_name:
            project_file = ProjectFile.objects.filter(
                project__name=project_name
            )
            return project_file

        return ProjectFile.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        project_files = self.get_queryset()

        if not project_files.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.get_serializer(project_files, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ProjectFileDetailGenericView(RetrieveDestroyAPIView):
    serializer_class = ProjectFileDetailSerializer

    def get_object(self):
        return get_object_or_404(ProjectFile, pk=self.kwargs['pk'])

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        file = self.get_object()

        serializer = self.get_serializer(file)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        file = self.get_object()

        try:
            delete_file(file_path=file.file_path.path)

        except Exception as e:
            return Response(
                data={"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            file.delete()

        return Response(
            data={
                "message": "File deleted successfully"
            },
            status=status.HTTP_200_OK
        )


#########################################################################################


class ProjectFileListAPIView(APIView):
    def get_objects(self, project_name=None):
        if project_name:
            project_file = ProjectFile.objects.filter(
                project__name=project_name
            )
            return project_file

        return ProjectFile.objects.all()

    def get(self, request: Request) -> Response:
        project_name = request.query_params.get('project')

        project_files = self.get_objects(project_name)

        if not project_files.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = AllProjectFilesSerializer(project_files, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        file_content = request.FILES["file"]
        project_id = request.data["project_id"]

        project = get_object_or_404(Project, pk=project_id)

        serializer = CreateProjectFileSerializer(
            data=request.data,
            context={
                "raw_file": file_content,
            }
        )

        if serializer.is_valid(raise_exception=True):
            project_file = serializer.save()
            project_file.project.set([project])

            return Response(
                data={
                    "message": "File upload successfully"
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
