# Generated by Django 4.1.13 on 2024-08-25 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailsOtpRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateField(default=datetime.datetime(2024, 8, 25, 10, 0, 11, 475812))),
                ('count', models.IntegerField(default=1)),
            ],
            options={
                'unique_together': {('email', 'date')},
            },
        ),
    ]
