# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-01 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_auto_20180202_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='completed',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
