# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 12:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adaptive_learning', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userconceptscore',
            name='marked_known',
        ),
    ]
