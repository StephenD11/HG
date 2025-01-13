from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from .forms import UserRegisterForm, LoginForm
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User

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
                return render(request, 'HGcity/login.html', {'form': form, 'error': 'Неверный логин или пароль!'})
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


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'HGcity/password_reset.html', {'form': form})


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
