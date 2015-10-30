# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0003_referendumuservote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referendumuservote',
            name='comment',
        ),
        migrations.AddField(
            model_name='referendumuservote',
            name='referendum',
            field=models.ForeignKey(default=5, to='referendums.Referendum'),
            preserve_default=False,
        ),
    ]
