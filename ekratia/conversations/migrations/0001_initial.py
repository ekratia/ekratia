# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threads', '0007_auto_20151028_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=25, verbose_name='Subject')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=1000, verbose_name='Message')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.OneToOneField(null=True, blank=True, to='threads.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
