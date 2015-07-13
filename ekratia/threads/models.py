from django.db import models

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


from django.db import models
from config.settings import common

import datetime

class Thread(models.Model):

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    #date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.description

class Comment(models.Model):
    content = models.CharField(max_length=30)
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    #date = models.DateTimeField(auto_now_add=True)
    #path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.description

