# Generated by Django 2.1.2 on 2019-08-01 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20190801_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='config',
            field=models.TextField(default='{"publish_end_time": 0, "publish_start_time": 0, "implement": {"staged": 0, "stage": {"title": "", "describe": "", "stage_start_time": 0, "stage_end_time": 0}}}'),
        ),
        migrations.AlterField(
            model_name='task',
            name='resource_links',
            field=models.TextField(blank=True, default='{}', null=True),
        ),
    ]
