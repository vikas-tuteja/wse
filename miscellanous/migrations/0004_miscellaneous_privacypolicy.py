# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-14 08:20
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miscellanous', '0003_miscellaneous_tnc'),
    ]

    operations = [
        migrations.AddField(
            model_name='miscellaneous',
            name='privacypolicy',
            field=ckeditor.fields.RichTextField(default=''),
            preserve_default=False,
        ),
    ]
