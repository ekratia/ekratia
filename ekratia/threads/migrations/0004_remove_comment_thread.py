# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0003_auto_20151009_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='thread',
        ),
    ]
