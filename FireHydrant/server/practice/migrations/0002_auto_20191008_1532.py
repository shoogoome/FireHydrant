# Generated by Django 2.1.2 on 2019-10-08 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_accountexhibition'),
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PracitceClassroomUser',
            new_name='PracticeClassroomUser',
        ),
        migrations.AlterModelOptions(
            name='practiceclassroom',
            options={'verbose_name': '爱阅读后台管理教室', 'verbose_name_plural': '爱阅读后台管理教室表'},
        ),
        migrations.AlterModelOptions(
            name='practiceclassroomuser',
            options={'verbose_name': '爱阅读后台管理教室使用', 'verbose_name_plural': '爱阅读后台管理教室使用表'},
        ),
    ]
