# Generated by Django 5.0.6 on 2024-08-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_order_id_alter_subscription_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='plans',
            field=models.CharField(choices=[('plan_F5eyGdYCvZPtON', 'Monthly - $8.99'), ('plan_F5ey2nnZwy5v8Q', '3 Months - £49.99'), ('plan_F5eyNlWXHig7YB', '6 Months - £74.99')], default='plan_F5ey2nnZwy5v8Q', max_length=100),
        ),
    ]
