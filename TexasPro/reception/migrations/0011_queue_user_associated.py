# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-09 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reception', '0010_doctor_cur_queue_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='user_associated',
            field=models.CharField(default=0, max_length=50),
        ),
    ]