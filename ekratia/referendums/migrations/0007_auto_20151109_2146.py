# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0006_auto_20151103_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='approved',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='referendum',
            name='comment_points',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='referendum',
            name='total_no',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='referendum',
            name='total_users',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='referendum',
            name='total_yes',
            field=models.FloatField(default=0.0),
        ),
    ]
