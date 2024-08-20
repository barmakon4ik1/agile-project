from rest_framework import serializers
from apps.projects.models import ProjectFile
from apps.projects.utils.upload_file_helpers import (
    check_extension,
    create_file_path,
    check_file_size,
    save_file
)


class AllProjectFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectFile
        fields = ('id', 'file_name', 'project')


class CreateProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ('file_name', 'file_path')

    def validate_file_name(self, value: str) -> str:
        if not value.isascii():
            raise serializers.ValidationError("Please, provide a valid file name.")
        if not check_extension(value):
            raise serializers.ValidationError(
                "Valid file extensions: ['.csv', '.doc', '.pdf', '.xlsx']"
            )
        return value

    def validate_file_path(self, value: str) -> str:
        if not check_extension(value):
            raise serializers.ValidationError(
                "Valid file extensions: ['.csv', '.doc', '.pdf', '.xlsx']"
            )
        return value

    def create(self, validated_data):
        file_path = create_file_path(file_name=validated_data['file_name'])
        raw_file = self.context['request'].FILES['file_path']
        if check_file_size(file=raw_file):
            save_file(file_path=file_path, file_content=raw_file)
            validated_data['file_path'] = file_path
            return ProjectFile.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("File size is too large (2 MB as maximum).")


# http://127.0.0.1:8000/api/v1/projects/files/
