# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0005_referendumuservote_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='points',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='referendumuservote',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
