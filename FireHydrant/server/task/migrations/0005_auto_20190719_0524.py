# Generated by Django 2.1.2 on 2019-07-19 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20190715_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='config',
            field=models.TextField(default='{"publish_end_time": 0, "implement": {"stage": {"describe": "", "title": "", "stage_end_time": 0, "stage_start_time": 0}, "staged": 0}, "publish_start_time": 0}'),
        ),
    ]
