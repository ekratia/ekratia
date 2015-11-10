# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.db import models

from avatar.util import get_primary_avatar

from ekratia.referendums.models import ReferendumUserVote

import networkx as nx

from ekratia.delegates.models import Delegate


class User(AbstractUser):
    rank = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.username

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
        return self.compute_pagerank(referendum)

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
        return self.rank if self.rank > 0 else self.compute_pagerank()

    def compute_pagerank(self, referendum=None):
        """
        Creates a graph and calculates the pagerank for this node.
        This will not be efficient in any manner, but should suffice
        until we need to optimize it with a better data structure.
        """
        graph = nx.DiGraph()

        visited, queue, user_ids = set(), [self.id], []

        if referendum:
            user_ids = ReferendumUserVote.objects.\
                        filter(referendum=referendum)\
                        .exclude(user=self).values_list('user_id', flat=True)

        while queue:
            current = queue.pop(0)
            # if current in user_ids:
            #     visited.add(current)
            #     count_exclude_users += 1
            #     continue

            if current not in visited:
                graph.add_node(current)
                delegates = Delegate.objects.filter(user__id=current)
                for delegate in delegates:
                    graph.add_node(delegate.delegate.id)
                    graph.add_edge(current, delegate.delegate.id)
                    queue.append(delegate.delegate.id)

                delegated_to_me = Delegate.objects\
                    .filter(delegate__id=current).exclude(user_id__in=user_ids)

                for delegate in delegated_to_me:
                    graph.add_node(delegate.user.id)
                    graph.add_edge(delegate.user.id, current)
                    queue.append(delegate.user.id)

                visited.add(current)

        pagerank_values = nx.pagerank_numpy(graph)
        num_visited = len(visited)

        # Update pagerank where necessary
        for user_id, rank in pagerank_values.iteritems():
            if referendum:
                try:
                    vote = ReferendumUserVote.objects.get(
                            user_id=user_id,
                            referendum=referendum)
                    vote.value = rank if vote.value > 0 else -rank
                    vote.save()
                except ReferendumUserVote.DoesNotExist:
                    pass
            else:
                user = User.objects.get(pk=user_id)
                new_rank = rank * num_visited
                if user.rank != new_rank:
                    user.rank = new_rank
                    user.save()

        if referendum:
            referendum.update_totals()

        self.rank = pagerank_values[self.id] * num_visited
        return self.rank

    def update_votes(self):
        # Update Votes on Referendums
        ReferendumUserVote.objects.open_votes(user=self, positive=True)\
            .update(value=self.rank)
        ReferendumUserVote.objects.open_votes(user=self, positive=False)\
            .update(value=-self.rank)

        # TODO: Update votes on comments
