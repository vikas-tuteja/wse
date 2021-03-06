# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-07 07:29
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20170824_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='overview',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='communication_criteria',
            field=models.CharField(blank=True, choices=[(b'1', b'Confident in English-speaking'), (b'2', b'Knows English but not confident'), (b'3', b'Confident in Hindi'), (b'4', b'Not much confident in speaking')], max_length=100, null=True),
        ),
    ]
