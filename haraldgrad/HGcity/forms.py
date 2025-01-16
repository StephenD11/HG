from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'hp', 'social_rating', 'wallet', 'ideology', 'logo']
        help_texts = {
            'username': 'С логином что-то не так, попробуй еще раз',
            'email': 'Явно не правильно написал email, исправляй',
            'password1': 'Введи надежный пароль',
            'password2': 'Повтори пароль',
        }

    # Валидация на уникальность Email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот Email уже зарегистрирован, попробуй другой')
        return email


class LoginForm(AuthenticationForm):
    pass


