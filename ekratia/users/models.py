# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
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
