# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from .views import ThreadListView, ThreadCreateView, ThreadDetailView


urlpatterns = [
    url(r'^$', ThreadListView.as_view(), name="threads"),
    url(r'^(?P<slug>[\w\-\:\.0-9\s]+)/$', ThreadDetailView.as_view(),
        name='detail'),
    url(r'^create$', ThreadCreateView.as_view(), name="create"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
