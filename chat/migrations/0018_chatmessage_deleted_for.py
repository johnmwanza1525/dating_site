# Generated by Django 5.1 on 2024-09-05 03:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_chatsession_user_deletion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='deleted_for',
            field=models.ManyToManyField(blank=True, related_name='deleted_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
