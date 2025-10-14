from django.apps import AppConfig
from rest_framework.settings import api_settings


class MyFirstAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_first_app"
    verbose_name = "Менеджер задач"

    # Пришлось форснуть перезагрузку DRF при старте приложения
    # без этого все мои глобальные настройки (JWTAuthentication и CursorPagination) терялись
    # rest_framework.settings.api_settings кем-то кэшируется до того, как мой REST_FRAMEWORK читается
    def ready(self):
        # Перечитаем глобальные настройки DRF
        api_settings.reload()
        # подключаем функции-обработчики к сигналам
        import my_first_app.signals
