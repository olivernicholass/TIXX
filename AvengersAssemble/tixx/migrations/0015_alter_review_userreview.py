# Generated by Django 5.0.3 on 2024-04-04 17:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tixx', '0014_review_userreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='userReview',
            field=models.ForeignKey(default='Anonymous', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]