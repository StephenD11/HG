from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import logout
from django.contrib import messages  # Импорт для использования flash-сообщений
from django.core.exceptions import PermissionDenied

@receiver(user_logged_in)
def check_ban_status(sender, request, user, **kwargs):
    if user.is_banned:
        logout(request)  # Выход из аккаунта
        messages.error(request, "Ваш аккаунт заблокирован.")  # Сообщение пользователю
        raise PermissionDenied("Ваш аккаунт заблокирован.")  # Останавливаем процесс логина
