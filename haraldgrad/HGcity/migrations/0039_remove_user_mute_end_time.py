# Generated by Django 5.1.4 on 2025-01-27 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0038_user_mute_end_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mute_end_time',
        ),
    ]
