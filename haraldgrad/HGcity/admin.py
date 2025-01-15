from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'hp', 'social_rating', 'wallet', 'ideology', 'logo')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('id', 'social_rating', 'wallet')
