from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    pin_code = forms.CharField(max_length=4, widget=forms.NumberInput, required=True, label="Пин код")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'hp', 'social_rating', 'wallet', 'ideology', 'logo', 'pin_code']
        help_texts = {
            'username': 'С логином что-то не так, попробуй еще раз',
            'email': 'Явно не правильно написал email, исправляй',
            'password1': 'Введи надежный пароль',
            'password2': 'Повтори пароль',
            'pin_code': 'Введи 4-значный пин код',
        }

    # Валидация на уникальность Email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот Email уже зарегистрирован, попробуй другой')
        return email

    # Валидация пин кода
    def clean_pin_code(self):
        pin_code = self.cleaned_data.get('pin_code')
        if not pin_code.isdigit() or len(pin_code) != 4:
            raise forms.ValidationError("Пин-код должен состоять из 4 цифр.")
        return pin_code


class LoginForm(AuthenticationForm):
    pass


