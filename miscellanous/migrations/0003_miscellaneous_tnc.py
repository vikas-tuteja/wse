# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-14 06:11
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miscellanous', '0002_auto_20170804_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='miscellaneous',
            name='tnc',
            field=ckeditor.fields.RichTextField(default=''),
            preserve_default=False,
        ),
    ]