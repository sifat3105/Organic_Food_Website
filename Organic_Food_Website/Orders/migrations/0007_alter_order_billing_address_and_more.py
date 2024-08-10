# Generated by Django 5.0.7 on 2024-08-10 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_Dashboard', '0003_alter_account_user'),
        ('Orders', '0006_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account_Dashboard.billingaddress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account_Dashboard.shippingaddress'),
        ),
    ]
