# Generated by Django 5.1.4 on 2025-01-20 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0022_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]
