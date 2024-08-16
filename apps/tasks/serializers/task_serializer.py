from typing import Any
from rest_framework import serializers
from django.utils import timezone
from apps.projects.models import Project
from apps.tasks.models import Task, Tag
from apps.tasks.choices.priorities import Priority
from datetime import datetime


class AllTasksSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    assignee = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'status',
            'priority',
            'project',
            'assignee',
            'deadline'
        )


class CreateTaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Project.objects.all(),
    )

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'priority',
            'project',
            'tags',
            'deadline'
        )

    def validate_name(self, value: str) -> str:
        if len(value) < 10:
            raise serializers.ValidationError(
                "The name of the task couldn't be less than 10 characters"
            )
        return value

    def validate_description(self, value: str) -> str:
        if len(value) < 50:
            raise serializers.ValidationError(
                "The description of the task couldn't be less than 50 characters"
            )
        return value

    def validate_priority(self, value: int) -> int:
        if value not in [val[0] for val in Priority.choices()]:
            raise serializers.ValidationError(
                "The priority of the task couldn't be one of the available options"
            )
        return value

    def validate_project(self, value: str) -> str:
        if not Project.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "The project with this name couldn't be found in the database"
            )
        return value

    def validate_tags(self, value: list[str, ...]) -> list[str, ...]:
        if not Tag.objects.filter(name__in=value).exists():
            raise serializers.ValidationError(
                "The tags couldn't be found in the database"
            )
        return value

    def validate_deadline(self, value: str) -> datetime:
        # делаем время с временной зоной:
        value = timezone.make_aware(value.replace(tzinfo=None), timezone.get_current_timezone())
        if value < timezone.now():
            raise serializers.ValidationError(
                "The deadline of the task couldn't be in the past"
            )
        return value

    def create(self, validated_data: dict[str, Any]) -> Task:
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for tag in tags:
            task.tags.add(tag)
        task.save()
        return task