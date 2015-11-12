# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0007_auto_20151109_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='total_votes',
            field=models.FloatField(default=0.0),
        ),
    ]
