# Generated by Django 5.0.3 on 2024-03-31 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tixx', '0006_user_firstname_user_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='adminCheck',
            field=models.BooleanField(default=False),
        ),
    ]
