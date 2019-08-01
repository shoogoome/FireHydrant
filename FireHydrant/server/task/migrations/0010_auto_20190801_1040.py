# Generated by Django 2.1.2 on 2019-08-01 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_auto_20190801_0800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskreport',
            name='resource_links',
        ),
        migrations.AlterField(
            model_name='task',
            name='config',
            field=models.TextField(default='{"implement": {"stage": {"describe": "", "stage_end_time": 0, "stage_start_time": 0, "title": ""}, "staged": 0}, "publish_end_time": 0, "publish_start_time": 0}'),
        ),
        migrations.AlterField(
            model_name='task',
            name='resource_links',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
