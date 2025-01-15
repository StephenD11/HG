from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'HGcity'  # Это задает пространство имен

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),  # Профиль
    path('choose_logo/', views.choose_logo, name='choose_logo'),
    path('rules/', views.rules, name='rules'),  # Правила
    path('profile/update/', views.update_profile, name='update_profile'),
    path('about/', views.about, name='about'),  # О проекте
    path('contact/', views.contact, name='contact'),  # Контакты

    # Восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='/password_reset/done/'), name='password_reset',),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
