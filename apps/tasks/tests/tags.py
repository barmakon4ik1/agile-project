from django.test import TestCase


class TagsTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertContains(response, "Welcome to my site!")


"""self.client – это экземпляр встроенного в Django тестового клиента,
предоставляющий методы для имитации запросов к приложению.
Этот клиент используется для тестирования наших представлений и URL адресов
при этом без необходимости запускать реальный сервер. Он позволяет отправлять
различные HTTP запросы GET, POST, PUT, DELETE и т.д.) и проверять ответы."""


