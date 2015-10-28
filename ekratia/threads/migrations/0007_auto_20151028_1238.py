# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0006_thread_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='user',
        ),
        migrations.RemoveField(
            model_name='threaduservote',
            name='thread',
        ),
        migrations.RemoveField(
            model_name='threaduservote',
            name='user',
        ),
        migrations.DeleteModel(
            name='Thread',
        ),
        migrations.DeleteModel(
            name='ThreadUserVote',
        ),
    ]
