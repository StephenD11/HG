from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils.timezone import now
from rest_framework import serializers

class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True, null=True, default='Имя', verbose_name='Имя персонажа')
    last_name = models.CharField(max_length=100, blank=True, null=True, default='Фамилия',verbose_name='Фамилия персонажа')
    email = models.EmailField(unique=True,verbose_name='Почта')
    hp = models.IntegerField(default=100, blank=True, null=True,verbose_name='Жизни')
    social_rating = models.IntegerField(default=0, blank=True, null=True,verbose_name='Соц.рейтинг')
    wallet = models.IntegerField(default=0, blank=True, null=True,verbose_name='Кошелек')
    pin_code = models.CharField(max_length=4, blank=True, null=True, verbose_name='Пин код')
    registration_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP адрес')
    ideology = models.CharField(
        max_length=20,
        choices=[
            ('Национализм', 'Национализм'),
            ('Социализм', 'Социализм'),
            ('Демократия', 'Демократия'),
            ('Монархизм', 'Монархизм')
        ],
        default='None',
        null=True, blank=True,
        verbose_name='Идеология'
    )
    logo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Логотип')
    last_name_change = models.DateTimeField(auto_now=True,verbose_name='Дата изменения имени')
    last_username_change = models.DateTimeField(auto_now=True,verbose_name='Дата изменения лого')
    is_banned = models.BooleanField(default=False,verbose_name='Бан')
    is_email_verified = models.BooleanField(default=False,verbose_name='Подтверждение почты')
    chat_verified = models.BooleanField(default=True,verbose_name='Доступ к чату')
    last_entry = models.DateTimeField(blank=True, null=True, verbose_name='Последний вход')
    factory_visits = models.IntegerField(default=0, verbose_name='Количество входов в фабрику')

    def can_enter(self):
        """Разрешает вход не более 3 раз за 24 часа, сбрасывая счетчик в 00:00"""
        # Сбросить счетчик каждый день в 00:00
        today_midnight = now().replace(hour=0, minute=0, second=0, microsecond=0)
        if self.last_entry and self.last_entry >= today_midnight:
            # Если последние посещения были в текущие сутки
            if self.factory_visits > 3:
                return False  # Превышен лимит посещений за день
        return True  # Вход разрешен

    def update_entry(self):
        """Обновляет время входа и счетчик посещений"""
        today_midnight = now().replace(hour=0, minute=0, second=0, microsecond=0)
        if self.last_entry is None or self.last_entry < today_midnight:
            self.factory_visits = 0  # Сбрасываем, если новый день
        self.factory_visits += 1
        self.last_entry = now()
        self.save(update_fields=['last_entry', 'factory_visits'])




    # Уникальные обратные связи
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    ROLE_CHOICES = [
        ('Житель', 'Житель'),
        ('ГОХ', 'ГОХ'),
        ('Капитан Гох', 'Капитан Гох'),
        ('Система', 'Система'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Житель',
        blank=False,
        verbose_name='Роль'

    )

    biography = models.TextField(
        max_length=5000,
        blank=False,
        null=True,
        default='Здесь может быть ваша биография...',
        verbose_name='Биография'
    )

    def __str__(self):
        return self.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Добавляем связь с пользователем
    username = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}: {self.message}'



class Banneded(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ban_info')
    reason = models.TextField(verbose_name='Причина')
    banned_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата бана')
    banned_by_username = models.CharField(max_length=255,verbose_name='Бан от')
    banned_by_role = models.CharField(max_length=255,verbose_name='Бан от Роли')

    class Meta:
        verbose_name = 'Бан'
        verbose_name_plural = 'Баны'

    def __str__(self):
        return f'{self.user.username} (Забанен: {self.banned_at} кем: {self.banned_by_username})'

