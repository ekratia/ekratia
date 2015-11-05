# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser

from avatar.util import get_primary_avatar

from ekratia.referendums.models import ReferendumUserVote

import networkx as nx

from ekratia.delegates.models import Delegate


class User(AbstractUser):

    def __unicode__(self):
        return self.get_full_name_or_username()

    def get_data_dictionary(self):
        return {
                'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'full_name': self.get_full_name(),
               }

    @property
    def get_avatar(self):
        """
        Gets avatar from Django Avatar or Facebook
        """
        if get_primary_avatar(self):
            return get_primary_avatar(self).avatar.url
        elif self.socialaccount_set.all().count() > 0:
            return self.change_picture_size(
                self.socialaccount_set.all()[0].get_avatar_url())
        else:
            return 'http://placehold.it/75x75/'

    @property
    def get_full_name_or_username(self):
        """
        Get Full Name or Username
        """
        if len(self.get_full_name()) > 0:
            return self.get_full_name()
        else:
            return self.username

    def vote_count_for_referendum(self, referendum):
        """
        Calculates vote value depending on Delegates
        """
        return self.get_pagerank()

    def get_vote_referendum(self, referendum):
        try:
            vote = ReferendumUserVote.objects.get(referendum=referendum,
                                                  user=self)
            return vote
        except ReferendumUserVote.DoesNotExist:
            return None

    def change_picture_size(self, url, width=70, height=70):
        """
        Change the facebook url to use a thumbnail
        """
        return url.split('?')[0] + u'?width=%i&height=%i' % (width, height)

    def get_pagerank(self):
        """
        Creates a graph and calculates the pagerank for this node.
        This will not be efficient in any manner, but should suffice
        until we need to optimize it with a better data structure.
        """
        graph = nx.DiGraph()

        visited, queue = set(), [self.id]
        while queue:
            current = queue.pop(0)
            if current not in visited:
                graph.add_node(current)
                delegates = Delegate.objects.filter(user__id=current)
                for delegate in delegates:
                    graph.add_node(delegate.delegate.id)
                    graph.add_edge(current, delegate.delegate.id)
                    queue.append(delegate.delegate.id)

                delegated_to_me = Delegate.objects.filter(delegate__id=current)
                for delegate in delegated_to_me:
                    graph.add_node(delegate.user.id)
                    graph.add_edge(delegate.user.id, current)
                    queue.append(delegate.user.id)

                visited.add(current)
        return nx.pagerank_numpy(graph)[self.id]*len(visited)
