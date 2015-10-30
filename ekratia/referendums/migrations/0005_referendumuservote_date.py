# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0004_auto_20151030_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendumuservote',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 7, 8, 9, 259304, tzinfo=utc)),
        ),
    ]
