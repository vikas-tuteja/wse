# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 15:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master', '0002_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_proficiency', models.CharField(blank=True, choices=[(b'pro', b'PRO'), (b'average', b'Average'), (b'poor', b'Poor')], max_length=50, null=True)),
                ('looks', models.CharField(blank=True, choices=[(b'class', b'Class'), (b'cool', b'Cool'), (b'average', b'Average')], max_length=50, null=True)),
                ('open_to_which_kind_of_job', models.CharField(blank=True, max_length=100, null=True)),
                ('pay_scale', models.CharField(blank=True, max_length=100, null=True)),
                ('comfortable_travelling_outdoor', models.BooleanField(default=False)),
                ('comfortable_for_liquor_promotion', models.BooleanField(default=False)),
                ('comfortable_working_at_odd_timings', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='ClientAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_address', models.CharField(blank=True, max_length=100, null=True)),
                ('establishment_year', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Client Attributes (to be filled only if user type is client)',
            },
        ),
        migrations.CreateModel(
            name='CordinatorAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_for', models.CharField(blank=True, choices=[(b'event-agencies', b'Event Agencies'), (b'clients', b'Clients')], max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Cordinator Attributes (to be filled only if user type is cordinator)',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.BigIntegerField()),
                ('whatsapp_number', models.BigIntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=users.models.uploadpath)),
                ('blacklist_flag', models.BooleanField(default=False)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Area')),
                ('auth_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.City')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.State')),
            ],
            options={
                'verbose_name': 'Users detail',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserRole'),
        ),
        migrations.AddField(
            model_name='cordinatorattribute',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
        migrations.AddField(
            model_name='clientattribute',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
        migrations.AddField(
            model_name='candidateattribute',
            name='candidate_profile',
            field=models.ManyToManyField(blank=True, null=True, to='users.CandidateType'),
        ),
        migrations.AddField(
            model_name='candidateattribute',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
    ]
