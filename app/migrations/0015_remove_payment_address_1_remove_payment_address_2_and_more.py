# Generated by Django 4.2.7 on 2024-01-12 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_payment_address_1_payment_address_2_payment_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='address_1',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='address_2',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='city',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order_comments',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='state',
        ),
    ]
