# Generated by Django 5.1.4 on 2025-01-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0026_alter_user_email_alter_user_first_name_alter_user_hp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_verified',
            field=models.BooleanField(default=False, verbose_name='Доступ к чату'),
        ),
    ]
