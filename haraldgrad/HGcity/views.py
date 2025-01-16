
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordResetForm
from .forms import UserRegisterForm, LoginForm
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User
from django.contrib.auth.decorators import login_required




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
                login(request, user)
                return redirect('HGcity:profile')  # Перенаправление на профиль
            else:
                # Ошибка аутентификации
                form.add_error(None, 'Неверный логин или пароль!')  # Добавление ошибки в форму
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
            return redirect('HGcity:profile')  # Перенаправление на профиль
    else:
        form = UserRegisterForm()
    return render(request, 'HGcity/register.html', {'form': form})


def home(request):
    return render(request, 'HGcity/home.html')


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



