# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-21 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20170820_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='education',
            field=models.CharField(blank=True, choices=[(b'10th', b'10th'), (b'12th', b'12th'), (b'graduate', b'Graduate')], max_length=100, null=True),
        ),
    ]