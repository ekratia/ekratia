# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .views import ReferendumListView, ReferendumCreateView,\
    ReferendumDetailView, ReferendumOpenView, ReferendumVoteView,\
    ReferendumProcessVoteView, ReferendumArchivedListView,\
    ReferendumResultsView


urlpatterns = [
    # Active Referendums
    url(r'^$', ReferendumListView.as_view(), name="list"),
    # Fnished Referendums
    url(r'^archived/$', ReferendumArchivedListView.as_view(), name="archived"),
    # Detail
    url(r'^(?P<slug>[\w\-\:\.0-9\s]+)/$', ReferendumDetailView.as_view(),
        name='detail'),
    # Referendum Results
    url(r'^(?P<slug>[\w\-\:\.0-9\s]+)/results/$',
        ReferendumResultsView.as_view(),
        name='results'),
    url(r'^create$', ReferendumCreateView.as_view(), name="create"),
    # View to Open Referendum for Votes
    url(r'^(?P<slug>[\w\-\:\.0-9\s]+)/open/$',
        ReferendumOpenView.as_view(), name="open"),
    # Page for Votes
    url(r'^(?P<slug>[\w\-\:\.0-9\s]+)/vote/$',
        ReferendumVoteView.as_view(), name="vote"),
    # Process Vote
    url(r'^(?P<slug>[\w\-\:\.0-9\s]+)/process/(?P<value>[\w\-\:\.0-9\s]+)/$',
        ReferendumProcessVoteView.as_view(), name="process_vote"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
