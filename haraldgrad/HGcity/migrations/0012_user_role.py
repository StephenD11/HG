# Generated by Django 5.1.4 on 2025-01-16 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0011_remove_complaint_message_remove_complaint_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Resident', 'Житель'), ('Moderator', 'ГОХ'), ('Government', 'Правительство')], default='Resident', max_length=20),
        ),
    ]
