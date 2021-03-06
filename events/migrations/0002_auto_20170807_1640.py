# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 16:40
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='eligibility',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='payments',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='selection_n_screening',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='t_n_c',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='venue_n_timing',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
