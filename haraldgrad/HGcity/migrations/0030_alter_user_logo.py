# Generated by Django 5.1.4 on 2025-01-20 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0029_alter_user_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Логотип'),
        ),
    ]
