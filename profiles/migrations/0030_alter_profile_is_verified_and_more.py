# Generated by Django 5.0.6 on 2024-08-22 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0029_alter_profile_is_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profileimage',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
