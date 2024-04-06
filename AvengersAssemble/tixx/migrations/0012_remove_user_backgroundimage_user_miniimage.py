# Generated by Django 5.0.3 on 2024-04-02 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tixx', '0011_user_backgroundimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='backgroundImage',
        ),
        migrations.AddField(
            model_name='user',
            name='miniImage',
            field=models.ImageField(blank=True, null=True, upload_to='mini_images/'),
        ),
    ]