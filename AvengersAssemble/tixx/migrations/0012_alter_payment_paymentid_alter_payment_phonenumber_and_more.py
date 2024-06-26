# Generated by Django 5.0.3 on 2024-04-09 21:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tixx', '0011_remove_payment_userid_payment_address_payment_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paymentId',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='phoneNumber',
            field=models.IntegerField(null=True),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='seatNum',
        ),
        migrations.AddField(
            model_name='payment',
            name='seatNum',
            field=models.ManyToManyField(blank=True, to='tixx.ticket'),
        ),
    ]
