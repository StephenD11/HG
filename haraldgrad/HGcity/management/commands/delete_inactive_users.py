from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Удаляет неактивированных пользователей старше 2 дней"

    def handle(self, *args, **kwargs):
        User = get_user_model()  # Получаем текущую модель пользователя
        threshold = now() - timedelta(days=0)
        deleted_count, _ = User.objects.filter(is_active=False, date_joined__lt=threshold).delete()
        self.stdout.write(f"Удалено {deleted_count} неактивированных пользователей.")
