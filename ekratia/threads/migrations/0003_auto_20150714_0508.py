# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0002_thread_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(max_length=250),
        ),
    ]
