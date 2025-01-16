from django.apps import AppConfig


class HgcityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HGcity'

    def ready(self):
        import HGcity.signals  # Импортируем файл signals