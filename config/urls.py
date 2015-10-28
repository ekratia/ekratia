# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'), name="about"),
    url(r'^rules/$',
        TemplateView.as_view(template_name='pages/rules.html'), name="rules"),

    url(r'^i-want-to-help/$',
        TemplateView.as_view(template_name='pages/i-want-to-help.html'),
        name="help"),

    # Django Admin
    url(r'^ekadmin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("ekratia.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Conversations
    url(r'^conversations/', include('ekratia.conversations.urls', namespace='conversations')),

    # Referendums
    url(r'^referendums/', include('ekratia.referendums.urls',
                                  namespace='referendums')),
    # Delegates App
    url(r'^delegates/', include('ekratia.delegates.urls',
                                namespace='delegates')),
    url(r'^avatar/', include('avatar.urls')),

    url(r'^api/v1/', include('ekratia.api.urls', namespace='api')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
