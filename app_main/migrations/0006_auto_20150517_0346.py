# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0005_auto_20150517_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentvote',
            name='weight',
            field=models.DecimalField(max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projecttopicweight',
            name='weight',
            field=models.DecimalField(max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='projectvote',
            name='weight',
            field=models.DecimalField(max_digits=3, decimal_places=2),
        ),
    ]
