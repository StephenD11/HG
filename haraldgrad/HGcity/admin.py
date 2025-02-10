from django.contrib import admin

from .models import User, Banneded


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'registration_ip', 'id', 'is_active', 'first_name', 'last_name','chat_verified', 'social_rating', 'ideology','role','is_banned')
    search_fields = ('username', 'first_name', 'is_banned', 'role', 'last_name', 'email', 'registration_ip')
    list_filter = ('ideology', 'role','is_banned','is_active')


@admin.register(Banneded)
class BannededAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'banned_at', 'banned_by_username', 'banned_by_role')  # Показываем нужные поля
    search_fields = ('user__username', 'banned_by_username', 'reason')  # Возможность поиска по имени пользователя, причине и забанившему
    list_filter = ('banned_by_role', 'banned_at')  # Фильтры по роли забанившего и дате

# Если хочешь добавить бан на страницу пользователя, можно сделать так:
class BannededInline(admin.TabularInline):
    model = Banneded
    fields = ('reason', 'banned_at', 'banned_by_username', 'banned_by_role')
    extra = 0  # Сколько пустых форм отображать