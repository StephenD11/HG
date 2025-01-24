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

    # Профиль и лого
    path('profile/', views.profile, name='profile'),
    path('choose_logo/', views.choose_logo, name='choose_logo'),

    path('update/', views.update, name='update'),  # Правила
    path('profile/update/', views.update_profile, name='update_profile'),
    path('about/', views.about, name='about'),  # О проекте
    path('contact/', views.contact, name='contact'),  # Контакты

    # Восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', success_url='/password_reset/done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', success_url='/reset/done/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    #Чат
    path('chat/', views.chat_view, name='chat'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/messages/', views.get_messages, name='get_messages'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
    path('chat_rules/', views.chat_rules, name='chat_rules'),

    #Подтверждение почты
    path('confirm_email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('confirm-your-email/', views.confirm_email_page, name='confirm_email_page'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)