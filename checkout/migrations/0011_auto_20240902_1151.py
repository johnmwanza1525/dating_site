# Generated by Django 3.2.25 on 2024-09-02 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_alter_order_plans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='pesapal_transaction_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='street_address1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='street_address2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='town_or_city',
        ),
    ]
