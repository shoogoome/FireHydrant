# Generated by Django 2.1.2 on 2019-08-01 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0012_auto_20190801_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='config',
            field=models.TextField(default='{}'),
        ),
    ]