# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-07 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='reception',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=3)),
                ('sex', models.CharField(max_length=2)),
            ],
        ),
    ]
