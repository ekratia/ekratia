# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .views import UserDelegatesView


urlpatterns = [
    url(r'^$', UserDelegatesView.as_view(), name="delegates"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
