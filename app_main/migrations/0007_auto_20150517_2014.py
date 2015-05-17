# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_main', '0006_auto_20150517_0346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thread', models.ForeignKey(to='app_main.Thread')),
            ],
        ),
        migrations.CreateModel(
            name='ProposalTopicWeight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.DecimalField(max_digits=3, decimal_places=2)),
                ('proposal', models.ForeignKey(to='app_main.Proposal')),
                ('topic', models.ForeignKey(to='app_main.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='ProposalVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.DecimalField(max_digits=3, decimal_places=2)),
                ('agree', models.BooleanField()),
                ('proposal', models.ForeignKey(to='app_main.Proposal')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='thread',
        ),
        migrations.RemoveField(
            model_name='project',
            name='topics',
        ),
        migrations.RemoveField(
            model_name='projecttopicweight',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projecttopicweight',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='projectvote',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectvote',
            name='user',
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='comment',
            field=models.ForeignKey(to='app_main.Proposal'),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='ProjectTopicWeight',
        ),
        migrations.DeleteModel(
            name='ProjectVote',
        ),
        migrations.AddField(
            model_name='proposal',
            name='topics',
            field=models.ManyToManyField(to='app_main.Topic', verbose_name=b'list of topics', through='app_main.ProposalTopicWeight'),
        ),
    ]
