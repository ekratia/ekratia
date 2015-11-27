# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_auto_20151112_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='num_comments',
            field=models.IntegerField(default=0),
        ),
    ]
