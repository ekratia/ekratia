# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0003_topic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='subtopic',
            field=models.ForeignKey(to='app_main.Topic'),
        ),
    ]
