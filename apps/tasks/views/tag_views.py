from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.tasks.models import Tag
from apps.tasks.serializers.tag_serializers import TagSerializer


class TagListAPIView(APIView):
    def get_objects(self) -> Tag:
        return Tag.objects.all()

    def get(self, request: Request) -> Response:
        tags = self.get_objects()

        if not tags.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = TagSerializer(tags, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TagDetailAPIView(APIView):
    def get_object(self, pk: int) -> Tag:
        return get_object_or_404(Tag, pk=pk)

    def get(self, request: Request, pk: int) -> Response:
        tag = self.get_object(pk=pk)

        serializer = TagSerializer(tag)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, pk: int) -> Response:
        tag = self.get_object(pk=pk)
        serializer = TagSerializer(tag, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, pk: int) -> Response:
        tag = self.get_object(pk=pk)

        tag.delete()

        return Response(
            data={
                "message": "Tag was deleted successfully"
            },
            status=status.HTTP_200_OK
        )
