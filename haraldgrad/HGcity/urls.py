from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

app_name = 'HGcity'  # Это задает пространство имен

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    path('guide/', views.guide_page, name='guide_page'),
    path('dont_work/', views.dont_work, name='dont_work'),
    path('support/', views.support_page, name='support_page'),


    # Регистрация
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("confirm_registration/<int:user_id>/", views.confirm_registration, name="confirm_registration"),


    # Профиль и лого
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('choose_logo/', views.choose_logo, name='choose_logo'),

    path('update/', views.update, name='update'),  # Правила
    path('profile/update/', views.update_profile, name='update_profile'),
    path('about/', views.about, name='about'),  # О проекте
    path('contact/', views.contact, name='contact'),  # Контакты
    path('about_close/', views.about_close, name='about_close'),  # О проекте

    # Восстановление пароля
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password_reset_complete/', views.password_reset_complete_view, name='password_reset_complete'),


    #Чат
    path('chat/', views.chat_view, name='chat'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/messages/', views.get_messages, name='get_messages'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
    path('chat_rules/', views.chat_rules, name='chat_rules'),

    #Статистика
    path('statistics/', views.statistics_view, name='statistics'),
    path('user/<int:user_id>/', views.user_detail_view, name='user_detail'),

    #Работы
    path('access_denied/', views.access_denied, name='access_denied'),  # Дополнительно, если доступ запрещен
    path('api/update_wallet/', views.update_wallet, name='update_wallet'),
    path('zavod/', views.zavod_view, name='zavod'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
