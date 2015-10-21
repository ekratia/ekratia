# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0005_auto_20151020_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='comment',
            field=models.OneToOneField(null=True, blank=True, to='threads.Comment'),
        ),
    ]
