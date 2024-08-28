from apps.users.models import User
from django.db import models
from apps.projects.models.project import Project
from apps.tasks.choices.statuses import Statuses
from apps.tasks.choices.priorities import Priority
from apps.tasks.utils.set_end_of_month import calculate_end_of_month


class Task(models.Model):
    name = models.CharField(
        max_length=120
    )
    description = models.TextField()
    status = models.CharField(
        max_length=15,
        choices=Statuses.choices,
        default=Statuses.NEW
    )
    priority = models.SmallIntegerField(
        choices=Priority,
        default=Priority.MEDIUM[0]
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    tags = models.ManyToManyField('Tag', related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(default=calculate_end_of_month)
    assignee = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-deadline']
        unique_together = ('name', 'project')

    def __str__(self):
        return f"{self.name}, status: {self.status}"
