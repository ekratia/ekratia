# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from ekratia.threads import api as threads

urlpatterns = patterns(
    '',
    url(r'^threads/$', threads.ThreadList.as_view()),
    url(r'^threads/(?P<pk>[0-9]+)/$', threads.ThreadDetail.as_view()),
    url(r'^comments/thread/(?P<pk>[0-9]+)/$',
        threads.ThreadComments.as_view()),
    url(r'^comments/$', threads.CommentList.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/$', threads.CommentDetail.as_view()),
    )
