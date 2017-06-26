# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def monkey_patch_auth():
    User._meta.get_field('email')._unique = True
    User._meta.get_field('email')._blank = False
    User._meta.get_field('email')._null = False

monkey_patch_auth()
