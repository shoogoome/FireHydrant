# Generated by Django 2.1.2 on 2019-08-15 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_accountexhibition'),
        ('task', '0014_auto_20190801_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskapply',
            name='exhibition',
        ),
        migrations.AddField(
            model_name='taskapply',
            name='exhibition',
            field=models.ManyToManyField(blank=True, null=True, related_name='task_account_exhibition', to='account.AccountExhibition'),
        ),
    ]