# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 04:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20170718_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocationstatus',
            name='application',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.RequirementApplication'),
        ),
    ]