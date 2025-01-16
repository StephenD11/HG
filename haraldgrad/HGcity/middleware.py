from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

class BanCheckMiddleware:
    """
    Middleware для проверки, забанен ли пользователь.
    Если забанен, разлогинивает и запрещает доступ.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_banned:
            logout(request)
            messages.error(request, "Ваш аккаунт заблокирован.")
            return redirect('login')  # Перенаправляем на страницу входа

        return self.get_response(request)
