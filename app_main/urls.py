# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from views import ThreadListView, ThreadCreate, DelegateView, ProposalView, VoteView

urlpatterns = [
    url(r'^threads/$', ThreadListView.as_view(template_name='app_main/threads.html'), name="threads"),
    url(r'^threads/create$', ThreadCreate.as_view(template_name='app_main/create_thread.html'), name="create-threads"),
    url(r'^thread/success$', TemplateView.as_view(template_name='app_main/success_thread.html'), name="success-thread"),

    url(r'^delegations$', DelegateView.as_view(template_name='app_main/delegations.html'), name="delegations"),
    url(r'^proposals/create$', ProposalView.as_view(template_name='app_main/create_proposal.html', success_url="/proposals/rule"), name="create_proposal"),
    url(r'^proposals/rule$', TemplateView.as_view(template_name='app_main/rule_proposal.html'), name="rule_proposal"),

    # url(r'^proposals/(?P<proposal_id>.*)/create$', ProposalView.as_view(template_name='app_main/create_proposal.html'), name="create_proposal"),
    # url(r'^proposals/(?P<proposal_id>.*)/rule$', VoteView.as_view(template_name='app_main/rule_proposal.html'), name="rule_proposal"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
