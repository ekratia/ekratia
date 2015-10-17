# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser

from avatar.util import get_primary_avatar
# from django.db import models
# from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    def __unicode__(self):
        return self.username

    def get_data_dictionary(self):
        return {
                'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'full_name': self.get_full_name(),
               }

    @property
    def get_avatar(self):
        if get_primary_avatar(self):
            return get_primary_avatar(self).avatar.url
        elif self.socialaccount_set.all().count() > 0:
            return self.change_picture_size(self.socialaccount_set.all()[0].get_avatar_url())
        else:
            return 'http://placehold.it/75x75/'

    def change_picture_size(self, url, width=70, height=70):
        return url.split('?')[0] + u'?width=%i&height=%i' % (width, height)
