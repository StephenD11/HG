from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'HGcity'  # Это задает пространство имен

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),  # Профиль
    path('choose_logo/', views.choose_logo, name='choose_logo'),
    path('rules/', views.rules, name='rules'),  # Правила
    path('about/', views.about, name='about'),  # О проекте
    path('contact/', views.contact, name='contact'),  # Контакты
    path('password_reset/', views.password_reset, name='password_reset'),  # Сброс пароля
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)