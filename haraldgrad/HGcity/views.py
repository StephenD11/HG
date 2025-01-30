from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserRegisterForm
from .models import User, Message, Banneded
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import time, random, re
from django.core.cache import cache  # Для временного хранения мута

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from datetime import datetime, time
from zoneinfo import ZoneInfo


class CustomLoginView(LoginView):
    template_name = 'HGcity/login.html'

    def form_valid(self, form):
        user = form.get_user()

        # Проверка: если пользователь не активен (например, email не подтвержден)
        if not user.is_active:
            form.add_error(None, "Ваш email не подтвержден. Пожалуйста, подтвердите его.")
            return self.form_invalid(form)

        # Проверка: если пользователь заблокирован
        if user.is_banned:
            messages.error(self.request,
                           "ВАШ АККАУНТ ЗАБЛОКИРОВАН | ЗАЯВКИ НА РАЗБЛОКИРОВКУ: SYSTEM.HARALDGRAD@GMAIL.COM")
            return redirect('HGcity:login')

        # Авторизация пользователя
        login(self.request, user)

        # Логика переадресации
        if user.logo:
            return redirect('HGcity:home')
        else:
            return redirect('HGcity:home')

    def get_success_url(self):
        """
        Этот метод все еще можно использовать, если не хочется переопределять `form_valid`.
        Но для кастомной логики лучше оставить его для дополнительной настройки.
        """
        return reverse('HGcity:home')


# Логин
def logout_view(request):
    logout(request)
    return redirect('HGcity:login')  # Перенаправляем на страницу логина после выхода


# Восстановление пароля
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('registration:password_reset_done')  # или нужный URL
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()

            # Отправляем письмо
            current_site = get_current_site(request)
            send_confirmation_email(user, current_site.domain)

            return redirect('HGcity:confirm_email_page')
    else:
        form = UserRegisterForm()

    return render(request, 'HGcity/register.html', {'form': form})


# Подтверждение почты
def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True  # Активируем пользователя
        user.save()
        return redirect('HGcity:login')  # Перенаправляем на страницу входа
    else:
        return render(request, 'HGcity/invalid_link.html')  # Показать ошибку, если токен невалиден


# Страница с уведомлением о необходимости подтверждения почты
def confirm_email_page(request):
    return render(request, 'registration/confirm_your_email.html')


# Функция отправки письма с подтверждением
def send_confirmation_email(user, domain):
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    subject = 'Подтвердите вашу почту'
    from_email = 'Система Харальдграда <system.haraldgrad@yandex.com>'
    to_email = [user.email]

    protocol = 'http'  # или 'https', если настроено на https

    text_content = f"Здравствуйте, {user.username}!\nПодтвердите почту: http://{domain}/confirm_email/{uid}/{token}/"
    html_content = render_to_string('registration/confirmation_email.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
        'protocol': protocol,  # Добавляем протокол в контекст
    })

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()


def home(request):
    User = get_user_model()
    user_count = User.objects.count()  # Считаем всех пользователей
    formatted_count = f"{user_count:04d}"  # Форматируем с 4 цифрами, дополняя нулями
    return render(request, 'HGcity/home.html', {'user_count': formatted_count})


def guide_page(request):
    return render(request, 'HGcity/guide_page.html')


def profile(request):
    return render(request, 'HGcity/profile.html')


def dont_work(request):
    return render(request, 'HGcity/dont_work.html')


def support_page(request):
    # Получаем 10 пользователей с наивысшим социальным рейтингом
    top_users = User.objects.order_by('-social_rating')[:10]
    return render(request, 'HGcity/support_page.html', {'top_users': top_users})


def update(request):
    return render(request, 'HGcity/update.html')


def about(request):
    return render(request, 'HGcity/about.html')


def profile_edit(request):
    return render(request, 'HGcity/profile_edit.html')


def contact(request):
    return render(request, 'HGcity/contact.html')


# Логотипы - выбор
@login_required
def choose_logo(request):
    # Инициализируем список логотипов
    logos = []

    # Определяем логотипы в зависимости от идеологии
    if request.user.ideology == 'Социализм':
        logos = [
            'logos/1level/cum_s_1 lvl_1.png',
            'logos/1level/cum_m_1 lvl_1.png',
            'logos/1level/cum_b_1 lvl_1.png',
        ]
    elif request.user.ideology == 'Национализм':
        logos = [
            'logos/1level/nac_s_1 lvl_1.png',
            'logos/1level/nac_m_1 lvl_1.png',
            'logos/1level/nac_b_1 lvl_1.png',
        ]
    elif request.user.ideology == 'Демократия':
        logos = [
            'logos/1level/dem_s_1 lvl_1.png',
            'logos/1level/dem_m_1 lvl_1.png',
            'logos/1level/dem_b_1 lvl_1.png',
        ]
    elif request.user.ideology == 'Монархизм':
        logos = [
            'logos/1level/mon_s_1 lvl_1.png',
            'logos/1level/mon_m_1 lvl_1.png',
            'logos/1level/mon_b_1 lvl_1.png',
        ]
    else:
        messages.error(request, "Для вашей идеологии нет доступных логотипов.")
        return redirect('HGcity:profile')  # Перенаправляем на профиль, если логотипов нет

    # Обрабатываем форму при отправке
    if request.method == 'POST':
        logo_choice = request.POST.get('logo')
        if logo_choice in logos:  # Проверяем, что выбранное лого находится в списке
            user = request.user
            user.logo = logo_choice  # Сохраняем выбранное лого в профиль пользователя
            user.save()
            messages.success(request, "Логотип успешно обновлен!")
            return redirect('HGcity:profile')  # Перенаправляем на профиль
        else:
            messages.error(request, "Выбран некорректный логотип.")

    # Отображаем форму выбора логотипа
    return render(request, 'HGcity/choose_logo.html', {'logos': logos})


# Обновить профиль
@login_required
def update_profile(request):
    if request.method == "POST":
        field = request.POST.get('field')
        value = request.POST.get('value')

        # Убираем лишние пробелы и новые строки в биографии
        if field == 'biography':
            value = value.strip()  # Удаляет пробелы в начале и конце
            value = ' '.join(value.split())  # Заменяет несколько пробелов на один

        # Поля, которые можно редактировать
        editable_fields = ['first_name', 'last_name', 'username', 'email', 'ideology', 'biography']

        if field in editable_fields:
            if field == 'biography':
                # Ограничим длину биографии (по модели)
                if len(value) <= 1000:
                    setattr(request.user, field, value)
            elif field == 'ideology':
                allowed_ideologies = ['Национализм', 'Социализм', 'Демократия', 'Монархизм']
                if value in allowed_ideologies:
                    setattr(request.user, field, value)
            else:
                setattr(request.user, field, value)

            # Сохраняем изменения
            request.user.save()

        # Отображаем обновленную страницу
        return render(request, 'HGcity/profile_edit.html', {'user': request.user})

    return render(request, 'HGcity/profile_edit.html', {'user': request.user})


# Профиль
def profile_view(request):
    if request.method == "POST" and "ideology" in request.POST:
        # Получаем выбранную идеологию
        selected_ideology = request.POST.get("ideology")
        # Проверяем, что идеология из списка допустимых значений
        if selected_ideology in ['Nationalism', 'Socialism', 'Democracy', 'Monarchism']:
            request.user.ideology = selected_ideology
            request.user.save()  # Сохраняем изменения
        return redirect('profile')  # Перезагрузка страницы профиля

    # Если запрос GET, просто отображаем профиль
    return render(request, 'HGcity/profile.html', {'user': request.user})


# chat.py


# чат
chat_messages = []
# Хранение данных о мутированных пользователях
muted_users = {}
MUTE_TIME = 60  # время мута в секундах
MAX_MESSAGES_COUNT = 25

# Маппинг для времени в секундах
time_mapping = {
    'm': 60,  # минута
    'h': 3600,  # час
}

# Список фраз с курсивом
drink_phrases = [
    "<i>выпил рюмку водки. Куда ты катишься, друг?</i>",
    "<i>не может остановиться! Выпив рюмку водки!</i>",
    "<i>снова за рюмкой, не может устоять!</i>",
    "<i>чувствует себя немного легче после еще одной рюмки водки.</i>",
    "<i>выпил рюмку. Сколько можно пить, а?</i>",
]


# Функция для обработки чата
@login_required
def chat_view(request):
    # Установить часовой пояс МСК
    msk_timezone = ZoneInfo('Europe/Moscow')
    current_time = datetime.now(msk_timezone).time()  # Текущее время в МСК

    # Ограничения на время доступа
    start_time = time(12, 0)  # 18:00
    end_time = time(23, 0)  # 23:00

    # Проверяем роль пользователя
    sender = request.user
    allowed_roles = ['Капитан Гох','ГОХ', 'Система']
    entrance = request.user.chat_verified

    # Ограничиваем доступ по времени, кроме определенных ролей
    if sender.role not in allowed_roles:
        if not (start_time <= current_time <= end_time) or entrance == 0:
            return render(request, 'HGcity/chat_closed.html', {
                'start_time': start_time,
                'end_time': end_time,
            })  # Показываем сообщение, если время вне диапазона и роль не разрешена

    # Если время подходит или пользователь имеет нужную роль, показываем чат
    return render(request, 'HGcity/chat.html')


# Функция для отправки сообщений
@login_required
def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        username = request.POST.get('username')

        # Ограничение на 250 символов
        if len(message_text) > 250:
            return JsonResponse({'status': 'error', 'message': 'Сообщение слишком длинное! Максимум 250 символов.'})

        # Если это команда /mute
        if message_text.startswith('/mute'):
            # Проверяем права отправителя
            sender = request.user
            if sender.role not in ['ГОХ', 'Капитан Гох', 'Система']:
                return JsonResponse({'status': 'error', 'message': 'У вас нет прав для выполнения этой команды.'})

            # Извлекаем логин и время мута
            parts = message_text.split(' ', 2)
            if len(parts) < 3:
                return JsonResponse(
                    {'status': 'error',
                     'message': 'Неверный формат команды. Используйте: /mute логин время(60, 180, 3600).'})

            target_username = parts[1]
            mute_duration = int(parts[2])  # Время в секундах (60, 180 или 3600)

            # Проверяем, что время мута допустимо
            if mute_duration not in [60, 180, 3600]:
                return JsonResponse(
                    {'status': 'error', 'message': 'Недопустимое время. Используйте 60, 180 или 3600.'})

            # Проверяем, существует ли пользователь
            try:
                target_user = User.objects.get(username=target_username)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'})

            # Если пользователь уже находится в муте, возвращаем ошибку
            if cache.get(f'muted_{target_user.username}'):
                return JsonResponse(
                    {'status': 'error', 'message': f'Пользователь {target_username} уже находится в муте.'})

            # Добавляем мут в кэш на заданное время
            cache.set(f'muted_{target_user.username}', True, mute_duration)

            # Отправляем сообщение в чат
            mute_message = f'Пользователь {sender.username} наложил мут на {target_username} на {mute_duration} секунд.'
            new_message = Message(user=sender, message=mute_message)
            new_message.save()

            return JsonResponse({'status': 'ok',
                                 'message': f'Пользователь {target_username} был замучен на {mute_duration} секунд.'})

        # Если это не команда, проверяем, есть ли мут у пользователя
        if cache.get(f'muted_{request.user.username}'):
            return JsonResponse(
                {'status': 'error', 'message': 'Вы не можете отправлять сообщения, так как находитесь в муте.'})

        # Если это команда /drink
        if message_text.startswith('/drink'):
            random_phrase = random.choice(drink_phrases)
            formatted_message = random_phrase.format(username=request.user.username)

            new_message = Message(user=request.user, message=formatted_message)
            new_message.save()

            return JsonResponse({'status': 'ok', 'message': formatted_message})

        # Если это команда /unban
        if message_text.startswith('/unban '):

            # Проверяем права отправителя
            sender = request.user
            if sender.role not in ['ГОХ', 'Капитан Гох', 'Система']:
                return JsonResponse({'status': 'error', 'message': 'У вас нет прав для выполнения этой команды.'})

            # Извлекаем логин пользователя, с которого нужно снять бан
            parts = message_text.split(' ', 1)
            if len(parts) < 2:
                return JsonResponse(
                    {'status': 'error', 'message': 'Неверный формат команды. Используйте: /unban логин.'})
            target_username = parts[1]

            # Проверяем, существует ли пользователь
            try:
                target_user = User.objects.get(username=target_username)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'})
            # Проверяем, забанен ли пользователь
            if not target_user.is_banned:
                return JsonResponse({'status': 'error', 'message': f'Пользователь {target_username} не забанен.'})

            # Удаляем запись о бане
            Banneded.objects.filter(user=target_user).delete()

            # Обновляем поле is_banned
            target_user.is_banned = False
            target_user.save()

            # Записываем сообщение в чат
            unban_message = f'Пользователь {sender.username} снял бан с {target_username}.'
            new_message = Message(user=sender, message=unban_message)
            new_message.save()
            return JsonResponse(
                {'status': 'ok', 'message': f'Пользователь {target_username} был разбанен.'})

        # Если это команда /ban
        if message_text.startswith('/ban '):
            # Проверяем права отправителя
            sender = request.user
            if sender.role not in ['Капитан Гох', 'Система']:
                return JsonResponse({'status': 'error', 'message': 'У вас нет прав для выполнения этой команды.'})

            # Извлекаем логин и причину
            parts = message_text.split(' ', 2)
            if len(parts) < 3:
                return JsonResponse(
                    {'status': 'error', 'message': 'Неверный формат команды. Используйте: /ban логин причина.'})

            target_username = parts[1]
            reason = parts[2]

            # Отладочное сообщение
            print(f"Команда /ban получена: target_username={target_username}, reason={reason}")

            # Проверяем, существует ли пользователь
            try:
                target_user = User.objects.get(username=target_username)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'})

            # Проверяем, забанен ли уже пользователь
            if target_user.is_banned:
                return JsonResponse({'status': 'error', 'message': f'Пользователь {target_username} уже забанен.'})

            # Создаем запись о бане
            Banneded.objects.create(
                user=target_user,
                reason=reason,
                banned_by_username=sender.username,
                banned_by_role=sender.role
            )

            # Обновляем поле is_banned
            target_user.is_banned = True
            target_user.save()

            # Записываем сообщение в чат
            ban_message = f'Пользователь {sender.username} забанил {target_username} по причине: {reason}'
            new_message = Message(user=sender, message=ban_message)
            new_message.save()

            return JsonResponse(
                {'status': 'ok', 'message': f'Пользователь {target_username} был забанен. Причина: {reason}'})

        # Если это не команда, сохраняем обычное сообщение
        new_message = Message(user=request.user, message=message_text)
        new_message.save()

        return JsonResponse({'status': 'ok', 'message': message_text})


@login_required
def get_messages(request):
    messages = Message.objects.all().order_by('timestamp')  # Сортировка по времени создания
    response = {
        'messages': [
            {
                'id': msg.id,
                'username': msg.user.username,  # Передаем логин пользователя
                'timestamp': msg.timestamp.strftime('%H:%M:%S'),
                'message': msg.message,
                'role': msg.user.role,  # Передаем роль пользователя
                'first_name': msg.user.first_name,
                'last_name': msg.user.last_name
            }
            for msg in messages
        ]
    }
    return JsonResponse(response)


# Очистка чата
@login_required
def clear_chat(request):
    if request.method == 'POST':
        # Проверка роли пользователя
        if request.user.role not in ['ГОХ', 'Капитан Гох','Система']:
            return JsonResponse({'status': 'error', 'message': 'У вас нет прав для выполнения этой операции.'})

        # Очистка всех сообщений чата
        Message.objects.all().delete()  # Удаляем все сообщения из базы данных

        return JsonResponse({'status': 'ok', 'message': 'Чат был очищен.'})


# Функция для изменения роли пользователя. Доступно только администраторам.
def change_user_role(admin_user, target_user, new_role):
    """
    Функция для изменения роли пользователя. Доступно только администраторам.
    """
    if not admin_user.is_staff:
        raise PermissionDenied("Только администратор может изменить роль пользователя.")

    # Проверяем, что новая роль — валидная
    valid_roles = dict(User.ROLE_CHOICES).keys()
    if new_role not in valid_roles:
        raise ValueError("Неверная роль.")

    # Обновляем роль пользователя
    target_user.role = new_role
    target_user.save()

    return target_user


# Правила чата
def chat_rules(request):
    return render(request, 'HGcity/chat_rules.html')


# БАН
def permission_denied_view(request, exception):
    messages.error(request, "ВАШ АККАУНТ ЗАБЛОКИРОВАН | ЗАЯВКИ НА РАЗБЛОКИРОВКУ: SYSTEM.HARALDGRAD@GMAIL.COM")
    return redirect('HGcity:login')
