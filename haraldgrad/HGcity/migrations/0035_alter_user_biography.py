# Generated by Django 5.1.4 on 2025-01-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0034_user_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='biography',
            field=models.TextField(blank=True, default='', max_length=1000, null=True, verbose_name='Биография'),
        ),
    ]
