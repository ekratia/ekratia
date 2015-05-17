# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0002_auto_20150516_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='description',
            new_name='content',
        ),
        migrations.AddField(
            model_name='comment',
            name='depth',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
