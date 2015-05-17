# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0007_auto_20150517_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2033, 5, 17, 20, 44, 15, 407805)),
        ),
        migrations.AddField(
            model_name='proposal',
            name='rule',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='summary',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
