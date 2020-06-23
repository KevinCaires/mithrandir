# Generated by Django 2.2.10 on 2020-06-21 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20200621_1758'),
        ('service_orders', '0004_remove_serviceorder_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='job_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobs.Job'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='need_certificate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='need_equipment',
            field=models.BooleanField(default=True),
        ),
    ]
