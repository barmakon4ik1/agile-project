from django.test import TestCase
from apps.users.serializers.user_serializers import RegisterUserSerializer, UserListSerializer
from apps.projects.models import Project
from apps.users.choices.positions import Positions
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.users.models import User
from unittest.mock import patch


# Получение списка пользователей
class UserListGenericViewTestCase(TestCase):
    def test_user_list(self):
        User.objects.bulk_create([
            User(username='malchikpupkin', email='malchik.pupkin@web.de'),
            User(username='sobolev', email='sobolev@gmail.com'),
            User(username='chegevara', email='che@cubapartizane.cu'),
        ])

        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)


# Регистрация
class RegisterUserGenericViewTestCase(TestCase):
    def setUp(self):
        self.url = '/api/v1/users/register/'
        self.data = {
            'username': 'malchikpupkin',
            'first_name': 'Malchik',
            'last_name': 'Pupkin',
            'email': 'malchik.pupkin@web.de',
            'position': 'DESIGNER',
            'password': 'malchikpupkin',
            're_password': 'malchikpupkin'
        }

    def test_user_register(self):
        response = self.client.post(self.url, self.data)
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_invalid_email(self):
        self.data['email'] = 'malchik.pupkin'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_user_register_invalid_position(self):
        self.data['position'] = 'NOPASARAN'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

    def test_user_register_password_mismatch(self):
        self.data['re_password'] = 'abrakadabra'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)


# Тесты на проверку валидации данных:
class RegisterUserSerializerTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'chegevara',
            'first_name': 'Che',
            'last_name': 'Gevara',
            'email': 'che@cubapartizane.cu',
            'position': "QA",
            'password': 'nopasaran',
            're_password': 'nopasaran'
        }

    # Регистрация нового пользователя
    def test_valid_user_data(self):
        serializer = RegisterUserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIsInstance(serializer.validated_data['username'], str)
        self.assertIsInstance(serializer.validated_data['first_name'], str)
        self.assertIsInstance(serializer.validated_data['last_name'], str)
        self.assertIsInstance(serializer.validated_data['email'], str)
        self.assertIsInstance(serializer.validated_data['position'], str)
        self.assertIsInstance(serializer.validated_data['password'], str)
        self.assertIsInstance(serializer.validated_data['re_password'], str)

    # ошибки валидации
    def test_valid_username(self):
        self.data['username'] = 'che.gevara'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'The username must be alphanumeric characters or have only _ symbol',
            [str(i) for i in serializer.errors['non_field_errors']])

    def test_valid_first_name(self):
        self.data['first_name'] = 'Che1'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'The first name must contain only alphabet symbols',
            [str(i) for i in serializer.errors['non_field_errors']])

    def test_valid_last_name(self):
        self.data['last_name'] = 'Gevara+'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'The last name must contain only alphabet symbols',
            [str(i) for i in serializer.errors['non_field_errors']])

    def test_valid_password(self):
        self.data['re_password'] = 'No_Pasaran!'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], 'Passwords don\'t match')


# BDD + TDD - Все тесты должны “падать”.
class UserDetailGenericViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='chegevara',
            first_name='Che',
            last_name='Gevara',
            email='che@cubapartizane.cu',
            phone='3222333222',
            position='QA',
            project=Project.objects.create(name='Project1')
        )

    # получения информации об определённом пользователе, ожидаемых полях и их типах данных.
    def test_user_detail_success(self):
        response = self.client.get(f'/api/v1/users/{self.user.pk}/')
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.data['username'], str)
        self.assertIsInstance(response.data['first_name'], str)
        self.assertIsInstance(response.data['last_name'], str)
        self.assertIsInstance(response.data['email'], str)
        self.assertIsInstance(response.data['phone'], str)
        self.assertIsInstance(response.data['position'], str)
        self.assertIsInstance(response.data['project'], str)

        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['phone'], self.user.phone)
        self.assertEqual(response.data['position'], self.user.position)
        self.assertEqual(response.data['project'], self.user.project.name)

    # передан несуществующий id.
    def test_user_detail_not_found(self):
        response = self.client.get('/api/v1/users/999/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.data)

# **********************************************************************


class UserAPITestCase(APITestCase):
    fixtures = ['apps/users/tests/user_fix.json']

    def setUp(self):
        self.client = APIClient()
        self.user_list_url = reverse('user-list')
        self.register_url = reverse('user-register')
        self.user_detail_url = lambda pk: reverse('user-detail', kwargs={'pk': pk})

    # Проверка получения списка всех пользователей
    def test_get_all_users(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    # Проверка получения списка всех пользователей по имени проекта
    def test_get_users_by_project_name(self):
        project_name = 'Test_project_1'
        url = reverse('user-list')
        response = self.client.get(url, {'project_name': project_name})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        for user_data in response.data:
            self.assertEqual(user_data['project'], project_name)

    # Проверка получения пустого списка пользователей(нужно подменить выходной QuerySet)
    @patch('apps.users.views.user_views.UserListGenericView.get_queryset')
    def test_get_empty_user_list(self, mock_get_queryset):
        mock_get_queryset.return_value = User.objects.none()
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, [])

    # Проверка работы сериализатора на правильное отображение данных списка пользователей
    def test_user_list_serializer(self):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        serialized_data = serializer.data
        for user_data, user in zip(serialized_data, users):
            self.assertEqual(user_data['first_name'], user.first_name)
            self.assertEqual(user_data['last_name'], user.last_name)
            self.assertEqual(user_data['email'], user.email)
            self.assertEqual(user_data['phone'], user.phone)
            self.assertEqual(user_data['last_login'], user.last_login)
            self.assertEqual(user_data['position'], user.position)

    # Проверка получения деталей конкретного пользователя по его ID.
    def test_get_user_detail(self):
        user_id = 1
        response = self.client.get(self.user_detail_url(user_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'chegevara')

    # Проверка создания нового пользователя с хорошими данными
    def test_create_user(self):
        data = {
            'username': 'chegevara',
            'first_name': 'Che',
            'last_name': 'Gevara',
            'email': 'che@cubapartizane.cu',
            'position': 'QA',
            'password': 'No_Pasaran!',
            're_password': 'No_Pasaran!'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='chegevara').exists())

    # Проверка создания нового пользователя с испорченными данными
    def test_create_user_with_invalid_data(self):
        data = {
            'username': 'malchik pupkin',
            'first_name': 'Malchik',
            'last_name': 'Pupkin',
            'email': 'malchik.pupkin@web.de',
            'position': 'DESIGNER',
            'password': 'pass',
            're_password': 'pass'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Проверка создания нового пользователя с пропуском обязательных данных
    def test_create_user_with_missing_data(self):
        url = reverse('user-register')  # Маршрут для создания нового пользователя
        data = {
            "username": "malchikpupkin",
            "first_name": "Malchik",
            "email": "malchik.pupkin@web.de",
            "position": "DESIGNER",
            "password": "password000",
            "re_password": "password000"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('last_name', response.dat)
