# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-21 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_requirement_education'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='show_on_site',
            field=models.BooleanField(default=False),
        ),
    ]
