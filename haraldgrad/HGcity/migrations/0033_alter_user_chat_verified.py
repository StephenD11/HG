# Generated by Django 5.1.4 on 2025-01-23 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0032_alter_banneded_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chat_verified',
            field=models.BooleanField(default=True, verbose_name='Доступ к чату'),
        ),
    ]
