# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0010_referendum_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='num_comments',
            field=models.IntegerField(default=0),
        ),
    ]
