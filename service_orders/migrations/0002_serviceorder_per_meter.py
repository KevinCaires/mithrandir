# Generated by Django 2.2.10 on 2020-04-16 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='per_meter',
            field=models.BooleanField(default=False),
        ),
    ]
