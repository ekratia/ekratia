# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0009_auto_20151112_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='status',
            field=models.CharField(default=b'created', max_length=10),
        ),
    ]
