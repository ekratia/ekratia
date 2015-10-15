# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='subtopic',
            new_name='parent',
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
