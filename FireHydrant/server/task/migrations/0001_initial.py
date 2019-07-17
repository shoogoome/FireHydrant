# Generated by Django 2.0.2 on 2019-07-11 02:11

import common.core.dao.time_stamp
import common.enum.task.stage
import common.enum.task.type
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(default='')),
                ('resource_links', models.TextField(blank=True, default='', null=True)),
                ('task_type', models.IntegerField(default=common.enum.task.type.TaskTypeEnum(0))),
                ('stage', models.IntegerField(default=common.enum.task.stage.TaskStageEnum(0))),
                ('config', models.TextField(default='{"publish_start_time": 0, "publish_end_time": 0, "implement": {}}')),
                ('create_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('update_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
            options={
                'verbose_name': '任务',
                'verbose_name_plural': '任务表',
            },
        ),
        migrations.CreateModel(
            name='TaskReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, default='')),
                ('create_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('update_time', common.core.dao.time_stamp.TimeStampField(default=0)),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Account')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
                ('workers', models.ManyToManyField(blank=True, related_name='task_workers', to='account.Account')),
            ],
            options={
                'verbose_name': '任务进度汇报',
                'verbose_name_plural': '任务进度汇报表',
            },
        ),
    ]
