# Generated by Django 5.0.6 on 2024-08-29 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_alter_order_plans'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('paypal', 'PayPal'), ('mpesa', 'Lipa na M-Pesa'), ('card', 'Credit/Debit Card')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='mpesa_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='plans',
            field=models.CharField(choices=[('plan_F5eyGdYCvZPtON', 'Monthly - $8.99'), ('plan_F5ey2nnZwy5v8Q', '3 Months - $24.99'), ('plan_F5eyNlWXHig7YB', '6 Months - $40.99')], default='plan_F5ey2nnZwy5v8Q', max_length=100),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
