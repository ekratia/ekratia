# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=30)),
                ('depth', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.PositiveIntegerField()),
                ('agree', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Delegate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delegate', models.ForeignKey(related_name='delegate_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTopicWeight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.PositiveIntegerField()),
                ('project', models.ForeignKey(to='app_main.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.PositiveIntegerField()),
                ('agree', models.BooleanField()),
                ('project', models.ForeignKey(to='app_main.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('subtopic', models.ForeignKey(to='app_main.Topic', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='projecttopicweight',
            name='topic',
            field=models.ForeignKey(to='app_main.Topic'),
        ),
        migrations.AddField(
            model_name='project',
            name='thread',
            field=models.ForeignKey(to='app_main.Thread'),
        ),
        migrations.AddField(
            model_name='project',
            name='topics',
            field=models.ManyToManyField(to='app_main.Topic', verbose_name=b'list of topics', through='app_main.ProjectTopicWeight'),
        ),
        migrations.AddField(
            model_name='delegate',
            name='topic',
            field=models.ForeignKey(to='app_main.Topic'),
        ),
        migrations.AddField(
            model_name='delegate',
            name='user',
            field=models.ForeignKey(related_name='user_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentvote',
            name='comment',
            field=models.ForeignKey(to='app_main.Project'),
        ),
        migrations.AddField(
            model_name='commentvote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(to='app_main.Thread'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
