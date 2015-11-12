# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0008_referendum_total_votes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referendum',
            options={'ordering': ['open_time', '-date']},
        ),
    ]
