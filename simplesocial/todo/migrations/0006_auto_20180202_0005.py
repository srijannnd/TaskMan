# Generated by Django 2.0 on 2018-02-01 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20180202_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='deadline',
            field=models.DateField(verbose_name='%d-%m-%Y'),
        ),
    ]