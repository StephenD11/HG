from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True, null=True, default='Без Имени')
    last_name = models.CharField(max_length=100, blank=True, null=True, default='Без Фамилии')
    email = models.EmailField(unique=True)
    hp = models.IntegerField(default=100, blank=True, null=True)
    social_rating = models.IntegerField(default=0, blank=True, null=True)
    wallet = models.IntegerField(default=0, blank=True, null=True)
    ideology = models.CharField(
        max_length=20,
        choices=[
            ('Nationalism', 'Национализм'),
            ('Socialism', 'Социализм'),
            ('Democracy', 'Демократия'),
            ('Monarchism', 'Монархизм')
        ],
        default='None',
        null=True, blank=True
    )
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    last_name_change = models.DateTimeField(auto_now=True)
    last_username_change = models.DateTimeField(auto_now=True)
    is_banned = models.BooleanField(default=False)

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
        ('Житель', 'Resident'),
        ('ГОХ', 'Moderator'),
        ('Правительство', 'Government'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Житель',
        blank=False,
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