from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users" # при добавлении нового приложения изменили на юзера из этого приложения
