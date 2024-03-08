# Generated by Django 5.0.3 on 2024-03-08 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eventName', models.CharField(max_length=100)),
                ('eventDate', models.DateField()),
                ('eventId', models.AutoField(primary_key=True, serialize=False)),
                ('eventLocation', models.CharField(max_length=100)),
                ('eventDescription', models.CharField(max_length=250)),
                ('eventStatus', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('userEmail', models.EmailField(max_length=254)),
                ('userPhoneNumber', models.CharField(max_length=10)),
                ('userAddress', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewId', models.AutoField(primary_key=True, serialize=False)),
                ('reviewRating', models.IntegerField()),
                ('reviewTitle', models.CharField(max_length=10)),
                ('reviewText', models.CharField(max_length=50)),
                ('reviewDate', models.DateField()),
                ('eventID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tixx.event')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketId', models.AutoField(primary_key=True, serialize=False)),
                ('seatNum', models.CharField(max_length=5)),
                ('ticketQR', models.CharField(max_length=250)),
                ('ticketPrice', models.IntegerField()),
                ('ticketType', models.CharField(max_length=10)),
                ('eventId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tixx.event')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('seatId', models.AutoField(primary_key=True, serialize=False)),
                ('seatNumber', models.IntegerField()),
                ('ticketId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tixx.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentId', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('paymentAmount', models.FloatField()),
                ('paymentMethod', models.CharField(max_length=10)),
                ('paymentDate', models.DateField()),
                ('transactionId', models.CharField(max_length=10)),
                ('userId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tixx.user')),
            ],
        ),
    ]
