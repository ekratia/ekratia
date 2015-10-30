# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='open_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
