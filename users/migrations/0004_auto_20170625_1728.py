# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 17:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170625_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([]),
        ),
    ]