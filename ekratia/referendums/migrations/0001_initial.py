# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0006_thread_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Referendum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=25, verbose_name='Subject')),
                ('slug', models.SlugField(unique=True)),
                ('text_remove_rules', models.TextField(max_length=1000, verbose_name='Text that this referendum will remove from our rules')),
                ('text_add_rules', models.TextField(max_length=1000, verbose_name='Text that this referendum will add to our rules')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.OneToOneField(null=True, blank=True, to='threads.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
