# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-07 12:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adaptive_learning', '0005_userquestionscore_time_taken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquestionscore',
            name='time_taken',
        ),
        migrations.AddField(
            model_name='userquestionscore',
            name='end_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
        migrations.AddField(
            model_name='userquestionscore',
            name='start_time',
            field=models.TimeField(default=datetime.time(16, 0)),
        ),
    ]
