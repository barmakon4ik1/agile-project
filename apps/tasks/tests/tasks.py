from datetime import timedelta, datetime
from django.test import TestCase
from django.utils import timezone
from apps.projects.models import Project
from apps.tasks.models import Tag, Task
from apps.tasks.serializers.task_serializers import CreateUpdateTaskSerializer, TaskDetailSerializer
from apps.users.models import User
from apps.tasks.choices.priorities import Priority


class CreateTaskTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description="Test description for the test project name for the Unit tests."
        )
        self.tag1 = Tag.objects.create(id=1, name='Backend')
        self.tag2 = Tag.objects.create(id=2, name='DevOPS')
        self.user = User.objects.create(
            username='test_user',
            first_name='test',
            last_name='uer',
            email='user@example.com',
            position="PRODUCT_OWNER",
            password='1q9i2w8u3e7y4r6t5'
        )

    def test_valid_task_data(self):
        valid_data = {
            'name': 'Valid Task Name',
            'description': 'This is a valid task description with more than 50 characters.',
            'priority': Priority.HIGH[0],
            'project': self.project.name,
            'tags': [1, 2],
            'deadline': timezone.now() + timedelta(days=10)
        }
        serializer = CreateUpdateTaskSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # проверка сериализатора
        self.assertIsInstance(serializer.validated_data['name'], str)  # проверка каждого поля
        self.assertIsInstance(serializer.validated_data['description'], str)
        self.assertIsInstance(serializer.validated_data['priority'], int)
        self.assertIsInstance(serializer.validated_data['project'], Project)
        self.assertIsInstance(serializer.validated_data['tags'], list)
        for tag in serializer.validated_data['tags']:
            self.assertIsInstance(tag, Tag)
        self.assertIsInstance(serializer.validated_data['deadline'], timezone.datetime)

    # Проверка на короткое название задачи
    def test_short_name(self):
        invalid_data = {
            'name': 'Short',
            'description': 'This is a valid task description with more than 50 characters.',
            'priority': Priority.HIGH[0],
            'project': self.project.name,
            'tags': [1, 2],
            'deadline': timezone.now() + timedelta(days=10)
        }
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())  # ожидаем False
        self.assertIn('name', serializer.errors)
        self.assertEqual(serializer.errors['name'][0], "The name of the task couldn't be less than 10 characters")

    # Проверка на короткое описание задачи
    def test_short_description(self):
        invalid_data = {
            'name': 'Valid Task Name',
            'description': 'Short description.',
            'priority': Priority.HIGH[0],
            'project': self.project.name,
            'tags': [1, 2],
            'deadline': timezone.now() + timedelta(days=10)
        }
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)
        self.assertEqual(serializer.errors['description'][0],
                         "The description of the task couldn't be less than 50 characters")

    # Проверка на невалидное значение поля приоритетности
    def test_invalid_priority(self):
        invalid_data = {
            'name': 'Valid Task Name',
            'description': 'This is a valid task description with more than 50 characters.',
            'priority': 99,  # Invalid priority
            'project': self.project.name,
            'tags': [1, 2],
            'deadline': timezone.now() + timedelta(days=10)
        }
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('priority', serializer.errors)
        self.assertEqual(serializer.errors['priority'][0],
                         '"99" is not a valid choice.')

    # Проверка на указание несуществующего проекта
    def test_nonexistent_project(self):
        invalid_data = {
            'name': 'Valid Task Name',
            'description': 'This is a valid task description with more than 50 characters.',
            'priority': Priority.HIGH[0],
            'project': 'Nonexistent Project',
            'tags': [1, 2],
            'deadline': timezone.now() + timedelta(days=10)
        }
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('project', serializer.errors)
        self.assertEqual(serializer.errors['project'][0],
                         'Object with name=Nonexistent Project does not exist.')

    # Проверка на указание несуществующего тега
    def test_nonexistent_tags(self):
        invalid_data = {
            'name': 'Valid Task Name',
            'description': 'This is a valid task description with more than 50 characters.',
            'priority': Priority.HIGH[0],
            'project': self.project.name,
            'tags': ['Nonexistent Tag'],
            'deadline': timezone.now() + timedelta(days=10)
            }
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tags', serializer.errors)
        self.assertEqual(serializer.errors['tags'][0],
                         'Incorrect type. Expected pk value, received str.')

    # Проверка на дедлайн - он в прошлом
    def test_past_deadline(self):
        invalid_data = {
            'name': 'Valid Task Name',
            'description': 'This is a valid task description with more than 50 characters.',
            'priority': Priority.HIGH[0],
            'project': self.project.name,
            'tags': [self.tag1.name, self.tag2.name],
            'deadline': timezone.now() - timedelta(days=1)  # Past date
        }
        serializer = CreateUpdateTaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('deadline', serializer.errors)
        self.assertEqual(serializer.errors['deadline'][0],
                         "The deadline of the task couldn't be in the past")


# Тестирование конкретного объекта по уникальному полю ID
class TaskDetailTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Test Project')
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')
        self.user = User.objects.create(
            username='test_user',
            first_name='test',
            last_name='uer',
            email='user@example.com',
            position="PRODUCT_OWNER",
            password='1q9i2w8u3e7y4r6t5'
        )
        self.task = Task.objects.create(
            name='Valid Task Name',
            description='This is a valid task description with more than 50 characters.',
            priority=Priority.HIGH[0],
            project=self.project,
            deadline=timezone.now() + timedelta(days=10),
            assignee=self.user
        )
        self.task.tags.add(self.tag1, self.tag2)

    def test_task_detail_serializer(self):
        serializer = TaskDetailSerializer(instance=self.task)
        data = serializer.data

        deadline_utc = datetime.strftime(
            self.task.deadline.astimezone(timezone.timezone.utc),
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )

        # Проверка корректности возвращаемых данных
        self.assertEqual(data['name'], self.task.name)
        self.assertEqual(data['description'], self.task.description)
        self.assertEqual(data['status'], self.task.status.name)
        self.assertEqual(data['priority'], self.task.priority)
        self.assertEqual(data['project']['name'], self.project.name)
        self.assertEqual(data['deadline'], deadline_utc)
        self.assertEqual(data['assignee'], 1)
        self.assertNotIn('updated_at', data)
        self.assertNotIn('deleted_at', data)

        # Проверка типов данных
        self.assertIsInstance(data['name'], str)
        self.assertIsInstance(data['description'], str)
        self.assertIsInstance(data['status'], str)
        self.assertIsInstance(data['priority'], int)
        self.assertIsInstance(data['project'], dict)
        self.assertIsInstance(data['deadline'], str)
        self.assertIsInstance(data['assignee'], int)

    def test_task_detail_serializer_tags(self):
        serializer = TaskDetailSerializer(instance=self.task)
        data = serializer.data

        # Проверка, что теги возвращаются корректно
        tag_names = [{'id': tag.id, 'name': tag.name} for tag in self.task.tags.all()]
        self.assertEqual(data['tags'], tag_names)

        # Проверка типов данных для тегов
        self.assertIsInstance(data['tags'], list)
        self.assertTrue(all(isinstance(tag, dict) for tag in data['tags']))



