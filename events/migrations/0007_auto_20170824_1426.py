# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-24 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_show_on_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='communication_criteria',
            field=models.CharField(blank=True, choices=[(1, b'Confident in English-speaking'), (2, b'Knows English but not confident'), (3, b'Confident in Hindi'), (4, b'Not much confident in speaking')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='education',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.HighestQualification'),
        ),
    ]
