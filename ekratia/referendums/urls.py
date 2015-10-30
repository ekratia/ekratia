# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .views import ReferendumListView, ReferendumCreateView,\
                   ReferendumDetailView, ReferendumOpenView


urlpatterns = [
    url(r'^$', ReferendumListView.as_view(), name="list"),
    url(r'^(?P<slug>[\w\-\:\.0-9\s]+)/$', ReferendumDetailView.as_view(),
        name='detail'),
    url(r'^create$', ReferendumCreateView.as_view(), name="create"),
    url(r'^open/(?P<slug>[\w\-\:\.0-9\s]+)/$', ReferendumOpenView.as_view(), name="open"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
