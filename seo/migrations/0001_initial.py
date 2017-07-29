# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regular_expression', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False)),
                ('path', models.CharField(help_text="Specify the path (URL) for this page (only if static data is to be displayed) or Specify the path's regular expression (only if same data is to be displayed for all regex matches)", max_length=250, unique=True)),
                ('title', models.TextField(blank=True, default='', help_text='This is the meta (page) title, that appears in the title bar.')),
                ('keywords', models.TextField(blank=True, default='', help_text='Comma-separated keywords for search engines.')),
                ('description', models.TextField(blank=True, default='', help_text='A short description, displayed in search results.')),
            ],
        ),
    ]
