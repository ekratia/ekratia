from django.db import models

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


from django.db import models
from config.settings import common
from django.utils.text import slugify
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


from datetime import datetime

class Thread(models.Model):

    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, db_index=True)
    description = models.CharField(max_length=1000)
    #date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        title = self.title
        self.slug = slugify(title)

        super(Thread, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }

        return reverse('threads:detail', kwargs=kwargs)

class Comment(models.Model):
    content = models.CharField(max_length=30)
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(common.AUTH_USER_MODEL)
    #date = models.DateTimeField(auto_now_add=True)
    #path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.content

