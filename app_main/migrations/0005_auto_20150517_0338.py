# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0004_auto_20150517_0336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='subtopic',
            field=models.ForeignKey(blank=True, to='app_main.Topic', null=True),
        ),
    ]
