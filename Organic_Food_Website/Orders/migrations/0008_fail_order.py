# Generated by Django 5.0.7 on 2024-08-10 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0007_alter_order_billing_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='fail_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
