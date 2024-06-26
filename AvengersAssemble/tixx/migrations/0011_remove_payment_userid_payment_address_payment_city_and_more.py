# Generated by Django 5.0.2 on 2024-04-08 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tixx", "0010_review_userreview"),
    ]

    operations = [
        migrations.RemoveField(model_name="payment", name="userId",),
        migrations.AddField(
            model_name="payment",
            name="Address",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="payment",
            name="city",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="payment",
            name="email",
            field=models.EmailField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="payment",
            name="eventId",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="tixx.event"
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="firstName",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="payment",
            name="lastName",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="payment",
            name="phoneNumber",
            field=models.IntegerField(blank=True, default=2508049001),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="payment",
            name="province",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="payment",
            name="seatNum",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tixx.ticket",
            ),
        ),
    ]
