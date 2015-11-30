# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0008_auto_20151112_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentuservote',
            name='value',
            field=models.FloatField(default=0.0),
        ),
    ]
