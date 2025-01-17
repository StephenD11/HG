
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserRegisterForm, LoginForm
from django.http import HttpResponse
from .models import User, Message
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import time, random

def choose_logo(request):
    if request.method == 'POST' and 'logo' in request.FILES:
        logo = request.FILES['logo']
        # Сохранить логотип пользователя
        user = request.user
        user.logo = logo
        user.save()
        return HttpResponse("Логотип обновлен успешно.")

    # Получаем все лого из каталога
    logos = User.objects.filter(logo__isnull=False)
    return render(request, 'choose_logo.html', {'logos': logos})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_banned:
                    messages.error(request, "Ваш аккаунт заблокирован.")
                    return redirect('HGcity:login')
                login(request, user)
                return redirect('HGcity:guide_page')
            else:
                form.add_error(None, 'Неверный логин или пароль!')
    else:
        form = LoginForm()

    return render(request, 'HGcity/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('HGcity:login')  # Перенаправляем на страницу логина после выхода


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Шифруем пароль
            user.save()
            login(request, user)  # Входим автоматически после регистрации
            return redirect('HGcity:home')  # Перенаправление на профиль
    else:
        form = UserRegisterForm()
    return render(request, 'HGcity/register.html', {'form': form})



def home(request):
    User = get_user_model()
    user_count = User.objects.count()  # Считаем всех пользователей
    formatted_count = f"{user_count:04d}"  # Форматируем с 4 цифрами, дополняя нулями
    return render(request, 'HGcity/home.html', {'user_count': formatted_count})


def guide_page(request):
    return render(request, 'HGcity/guide_page.html')

def profile(request):
    return render(request, 'HGcity/profile.html')


def rules(request):
    return render(request, 'HGcity/rules.html')


def about(request):
    return render(request, 'HGcity/about.html')


def contact(request):
    return render(request, 'HGcity/contact.html')


@login_required
def update_profile(request):
    if request.method == "POST":
        field = request.POST.get('field')  # получаем имя поля, которое нужно обновить
        value = request.POST.get('value')  # получаем новое значение для поля

        # Проверка на допустимые поля
        if field in ['first_name', 'last_name', 'username', 'email', 'ideology']:
            if field == 'ideology':  # Если обновляем идеологию
                # Проверяем, что значение идеологии корректное
                if value in ['Nationalism', 'Socialism', 'Democracy', 'Monarchism']:
                    setattr(request.user, field, value)  # сохраняем новое значение
            else:
                setattr(request.user, field, value)  # сохраняем новое значение
            request.user.save()  # сохраняем изменения в базе данных

        return redirect('HGcity:profile')  # редирект на страницу профиля

    return render(request, 'HGcity/profile.html')



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


# Логотипы - выбор
@login_required
def choose_logo(request):
    if request.method == 'POST' and 'logo' in request.POST:
        logo_choice = request.POST['logo']

        # Сохранить логотип пользователя
        user = request.user
        user.logo = f'logos/{logo_choice}'  # Сохраняем путь
        user.save()
        return redirect('HGcity:profile')  # Перенаправляем на профиль

    logos = ['1.png', '2.png', '3.png', '4.png',]  # Пример списка логотипов
    return render(request, 'HGcity/choose_logo.html', {'logos': logos})


#чат
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

def chat_view(request):
    return render(request, 'HGcity/chat.html')


import re
import time

# Маппинг для времени в секундах
time_mapping = {
    'm': 60,  # минута
    'h': 3600,  # час
}

# Функция для отправки сообщений
import re
import time

# Маппинг для времени в секундах
time_mapping = {
    'm': 60,  # минута
    'h': 3600,  # час
}

# Функция для отправки сообщений
@login_required
def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        username = request.POST.get('username')

        # Ограничение на 250 символов
        if len(message_text) > 250:
            return JsonResponse({'status': 'error', 'message': 'Сообщение слишком длинное! Максимум 250 символов.'})

        # Проверка на мут
        if username in muted_users and time.time() < muted_users[username]:
            # Рассчитываем оставшееся время мута
            mute_time_left = muted_users[username] - time.time()

            # Определяем единицу времени для вывода
            if mute_time_left < 60:
                mute_message = f'Ты замучен на {int(mute_time_left)} секунд! Палкой по жопе!'
            else:
                mute_minutes = mute_time_left // 60
                if mute_minutes == 1:
                    mute_message = 'Ты замучен на 1 минуту! Палкой по жопе!'
                elif mute_minutes > 1 and mute_minutes < 60:
                    mute_message = f'Ты замучен на {int(mute_minutes)} минут! Палкой по жопе!'
                else:
                    mute_hours = mute_minutes // 60
                    mute_message = f'Ты замучен на {int(mute_hours)} час! Палкой по жопе!'

            return JsonResponse({'status': 'error', 'message': mute_message})

        # Если это команда /drink, генерируем сообщение, но не сохраняем команду
        if message_text.startswith('/drink'):
            random_phrase = random.choice(drink_phrases)
            formatted_message = random_phrase.format(username=request.user.username)

            # Сохраняем только отформатированное сообщение без команды
            new_message = Message(user=request.user, message=formatted_message)
            new_message.save()

            return JsonResponse({'status': 'ok', 'message': formatted_message})

        # Если это команда /mute с временем
        if message_text.startswith('/mute '):
            # Извлекаем время и пользователя из команды /mute
            parts = message_text.split(' ')
            time_match = re.match(r'(\d+)(m|h)', parts[1])  # Ищем числа с m (минуты) или h (часы)

            if time_match:
                mute_duration = int(time_match.group(1)) * time_mapping[time_match.group(2)]  # Переводим в секунды
                target_user = parts[2]  # Извлекаем имя пользователя для мута

                # Проверка на роль отправителя
                sender = request.user
                if sender.role not in ['ГОХ', 'Правительство']:
                    return JsonResponse({'status': 'error', 'message': 'У вас нет прав для выполнения этой команды.'})

                # Мутим указанного пользователя
                muted_users[target_user] = time.time() + mute_duration
                return JsonResponse({'status': 'ok', 'message': f'Пользователь {target_user} был замучен на {mute_duration} секунд.'})

            else:
                return JsonResponse({'status': 'error', 'message': 'Неверный формат времени. Используйте /mute 1m, /mute 3m, /mute 1h.'})

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


@login_required
def clear_chat(request):
    if request.method == 'POST':
        # Проверка роли пользователя
        if request.user.role not in ['ГОХ', 'Правительство']:
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


def chat_rules(request):
    return render(request, 'HGcity/chat_rules.html')



#БАН
def permission_denied_view(request, exception):
    messages.error(request, "Доступ запрещён: ваш аккаунт заблокирован.")
    return redirect('HGcity:login')


