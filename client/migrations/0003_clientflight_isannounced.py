# Generated by Django 2.0 on 2018-01-10 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20180108_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientflight',
            name='isAnnounced',
            field=models.BooleanField(default=False),
        ),
    ]