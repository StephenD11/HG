# Generated by Django 5.1.4 on 2025-02-11 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0047_alter_user_biography'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='username',
        ),
    ]
