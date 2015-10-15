# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_auto_20151012_2320'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delegate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delegate', models.ForeignKey(related_name='delegate_set', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(blank=True, to='topics.Topic', null=True)),
                ('user', models.ForeignKey(related_name='user_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
