# Generated by Django 2.2.10 on 2020-04-16 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('per_merter', models.BooleanField()),
                ('value_per_meter', models.FloatField()),
                ('job_group', models.CharField(max_length=50)),
            ],
        ),
    ]
