# Generated by Django 5.1.4 on 2025-01-16 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0009_chatmessage_alter_user_ideology_complaint'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.AlterModelOptions(
            name='complaint',
            options={'verbose_name': 'Жалоба', 'verbose_name_plural': 'Жалобы'},
        ),
    ]
