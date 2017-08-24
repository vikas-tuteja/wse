# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return self.name


class HighestQualification(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name
