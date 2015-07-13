# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from .views import ThreadListView, ThreadCreate


urlpatterns = [
    url(r'^$', ThreadListView.as_view(template_name='app_main/threads.html'), name="threads"),
    url(r'^create$', ThreadCreate.as_view(template_name='app_main/create_thread.html'), name="create-threads"),
    url(r'^success$', TemplateView.as_view(template_name='app_main/success_thread.html'), name="success-thread"),

    # url(r'^api/v1/threads/$', ThreadList.as_view()),
    # url(r'^api/v1/threads/(?P<pk>[0-9]+)/$', ThreadDetail.as_view()),
    # url(r'^api/v1/comments/thread/(?P<pk>[0-9]+)/$', CommentList.as_view()),
    # url(r'^api/v1/comments/$', CommentList.as_view()),
    # url(r'^api/v1/comments/(?P<pk>[0-9]+)/$', CommentDetail.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
