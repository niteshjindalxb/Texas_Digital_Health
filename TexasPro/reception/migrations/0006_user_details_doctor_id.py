# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-08 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reception', '0005_auto_20180307_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='doctor_id',
            field=models.CharField(default='NA', max_length=50),
        ),
    ]
