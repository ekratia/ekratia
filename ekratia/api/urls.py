# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from ekratia.threads import api as threads
from ekratia.conversations import api as conversations
from ekratia.referendums import api as referendums
from ekratia.delegates import api as delegates
from ekratia.users import api as users

urlpatterns = [
    # Conversations CRUD
    url(r'^conversations/$', conversations.ThreadList.as_view()),
    url(r'^conversations/(?P<pk>[0-9]+)/$',
        conversations.ThreadDetail.as_view()),
    # Comments CRUD
    url(r'^comments/$', threads.CommentList.as_view()),
    # Threads comments
    url(r'^comments/thread/(?P<pk>[0-9]+)/$',
        threads.ThreadComments.as_view()),
    # Referendums
    url(r'^referendums/$', referendums.ReferendumsList.as_view()),
    # Referendums Comments
    url(r'^comments/referendum/(?P<pk>[0-9]+)/$',
        referendums.ReferendumComments.as_view()),
    # ReferendumVoteGraph
    url(r'^referendum/(?P<pk>[0-9]+)/graph/$',
        referendums.ReferendumVoteGraph.as_view(), name="graph"),
    # Comments
    url(r'^comments/(?P<pk>[0-9]+)/$', threads.CommentDetail.as_view()),
    url(r'^comments/votes/$', threads.ThreadCommentsVotes.as_view()),
    # Delegates
    url(r'^delegates/$', delegates.AssignedDelegates.as_view()),
    url(r'^delegates/available/$', delegates.AvailableDelegates.as_view()),
    url(r'^delegates/(?P<delegate_id>[0-9]+)/$',
        delegates.UserDelegateDetail.as_view()),
    # Users
    url(r'^users/(?P<pk>[0-9]+)/$',
        users.UserView.as_view()),
]
