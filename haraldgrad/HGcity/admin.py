from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'first_name', 'last_name', 'email', 'hp', 'social_rating', 'wallet', 'ideology', 'logo','role')
    search_fields = ('username', 'first_name', 'is_banned', 'role', 'last_name', 'email')
    list_filter = ('id', 'social_rating', 'wallet')

    # Определяем редактирование ролей в админке
    fieldsets = ((None, {'fields': ('username', 'role', 'email', 'password', 'first_name', 'last_name','is_banned')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),)

