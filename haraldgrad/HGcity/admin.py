from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'first_name', 'last_name','chat_verified', 'hp', 'social_rating', 'ideology', 'logo','role')
    search_fields = ('username', 'first_name', 'is_banned', 'role', 'last_name', 'email')
    list_filter = ('ideology', 'role')



