# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0009_auto_20151130_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]
