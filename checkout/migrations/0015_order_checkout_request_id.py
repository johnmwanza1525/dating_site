# Generated by Django 3.2.25 on 2024-09-02 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0014_auto_20240902_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout_request_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
