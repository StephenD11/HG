# Generated by Django 5.1.4 on 2025-02-11 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HGcity', '0048_remove_message_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='username',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]
