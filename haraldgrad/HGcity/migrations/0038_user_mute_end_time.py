# Generated by Django 5.1.4 on 2025-01-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0037_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mute_end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
