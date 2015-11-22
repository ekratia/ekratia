# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.db import models

from avatar.util import get_primary_avatar
import networkx as nx

from ekratia.core.graphs import get_graph_value, GraphEkratia
from ekratia.delegates.models import Delegate
from ekratia.referendums.models import Referendum, ReferendumUserVote

import logging
logger = logging.getLogger('ekratia')


class User(AbstractUser):
    rank = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.username

    def get_data_dictionary(self):
        """
        Return dictionary with basic information of the user
        """
        return {
                'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'full_name': self.get_full_name(),
               }

    def get_available_delegates(self, name=None):
        queryset = User.objects.exclude(
                                id__in=Delegate.objects.filter(
                                    user_id=self.id)
                                .values_list('delegate_id'))\
                               .exclude(id=self.id)
        if name is not None:
            queryset = queryset.filter(username__icontains=name)
        return queryset

    def get_users_delegated_to_me(self):
        return User.objects.filter(
            id__in=Delegate.objects.filter(
                delegate=self).values_list('user_id'))

    def get_users_delegated_by_me(self):
        return User.objects.filter(
            id__in=Delegate.objects.filter(
                user=self).values_list('delegate_id'))

    def delegate_to(self, user):
        """
        Creates a delegated user
        Return the Delegate object
        """
        if isinstance(user, int):
            try:
                user = User.objects.get(id=user)
            except User.DoesNotExist:
                raise ValueError("User not found")
        elif not isinstance(user, User):
            raise ValueError("Not an User instance")
        elif self == user:
            raise ValueError("User can not delegate itself")

        return Delegate.objects.create(user=self, delegate=user)

    def undelegate_to(self, user):
        """
        Undelegate an user
        Returns True if success
        """
        if isinstance(user, int):
            try:
                user = User.objects.get(id=user)
            except User.DoesNotExist:
                raise ValueError("User not found")
        elif not isinstance(user, User):
            raise ValueError("Not an User instance")

        try:
            delegate = Delegate.objects.get(user=self, delegate=user)
            delegate.delete()
        except Delegate.DoesNotExist:
            return False
        return True

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
        # My weight vote value
        count = self.get_pagerank_value_referendum(referendum)

        # # value given by users that delegated to me
        # for user in self.get_users_delegated_to_me():
        #     count = count + user.get_pagerank_value_referendum(referendum)

        # # value given by delegates
        # for user in self.get_users_delegated_by_me():
        #     count = count + user.get_pagerank_value_referendum(referendum)

        return count

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

    def compute_pagerank(self):
        self.rank = self.get_pagerank_value()
        self.save()

    def compute_pagerank_tuple(self):
        """
        Creates a graph and calculates the pagerank for this node.
        This will not be efficient in any manner, but should suffice
        until we need to optimize it with a better data structure.
        """
        graph = nx.DiGraph()
        logger.debug("Calculate pagerank for %s" % self)

        visited, queue = set(), [self.id]
        while queue:
            current = queue.pop(0)
            logger.debug('Current graph: %s' % current)
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

        pagerank_values = nx.pagerank_numpy(graph)
        num_visited = len(visited)
        for user_id, rank in pagerank_values.iteritems():
            user = User.objects.get(pk=user_id)
            new_rank = rank * num_visited
            if user.rank != new_rank:
                user.rank = new_rank
                user.save()

        self.rank = pagerank_values[self.id]*num_visited
        return self.rank, pagerank_values

    def compute_pagerank_referendum(self, referendum=None):
        delegaters = Delegate.objects.filter(delegate=self)
        user_ids = ReferendumUserVote.objects\
            .filter(referendum=referendum)\
            .exclude(user=self)\
            .values_list('user_id', flat=True)
        delegaters = delegaters.exclude(delegate_id__in=user_ids)
        count_excluded_delegaters = delegaters.count()
        rank, values = self.compute_pagerank_tuple()
        return rank * (len(values) - count_excluded_delegaters + 1)

    def compute_pagerank_referendum_2(self, referendum=None):
        logger.debug("Calculate pagerank for %s" % self)
        graph = nx.DiGraph()

        visited, queue, user_ids, count_missing_vote = set(), [self.id], [], 0

        if referendum:
            logger.debug("Referendum: %s" % referendum.title)
            user_ids = ReferendumUserVote.objects\
                .filter(referendum=referendum)\
                .exclude(user=self)\
                .values_list('user_id', flat=True)
            logger.debug("Users with votes: %s" % str(user_ids))

        while queue:
            current = queue.pop(0)
            if current not in visited:
                graph.add_node(current)
                logger.debug('Current graph: %s' % current)

                if current in user_ids:
                    count_missing_vote -= 1

                delegates = Delegate.objects\
                    .filter(user__id=current)
                for delegate in delegates:
                    logger.debug("Current Delegate: %s" % delegate.delegate.id)
                    if len(user_ids) > 0 and delegate.delegate.id in user_ids:
                        count_missing_vote += 1
                        logger.info("delegate in user_ids")
                    else:
                        graph.add_node(delegate.delegate.id)
                        graph.add_edge(current, delegate.delegate.id)
                        queue.append(delegate.delegate.id)

                delegated_to_me = Delegate.objects\
                    .filter(delegate__id=current)

                for delegate in delegated_to_me:
                    logger.debug("Current Delegated: %s" % delegate.user.id)
                    if len(user_ids) > 0 and delegate.user.id in user_ids:
                        count_missing_vote += 1
                        logger.info("delegated_to_me in user_ids")
                    else:
                        graph.add_node(delegate.user.id)
                        graph.add_edge(delegate.user.id, current)
                        queue.append(delegate.user.id)

                visited.add(current)

        pagerank_values = nx.pagerank_numpy(graph)
        num_visited = len(visited) + count_missing_vote

        logger.debug("Pagerank values: %s" % str(pagerank_values))
        logger.debug("Visited: %s" % num_visited)

        # Update pagerank where necessary
        for user_id, rank in pagerank_values.iteritems():
            if referendum:
                try:
                    vote = ReferendumUserVote.objects.get(
                            user_id=user_id,
                            referendum=referendum)
                    rank_value = rank * num_visited
                    vote.value = rank_value if vote.value > 0 else -rank_value
                    vote.save()
                except ReferendumUserVote.DoesNotExist:
                    pass
            else:
                user = User.objects.get(pk=user_id)
                new_rank = rank * num_visited
                logger.debug('New rank for %s: %s' % (user.username, new_rank))
                if user.rank != new_rank:
                    user.rank = new_rank
                    user.save()

        if referendum:
            referendum.update_totals()
        self.rank = pagerank_values[self.id] * num_visited
        if not referendum:
            self.save()
        return self.rank

    def update_votes(self):
        # Update Votes on Referendums
        referendum_ids = ReferendumUserVote.objects.open_votes(user=self)\
            .values_list('referendum_id', flat=True)
        referendums = Referendum.objects.filter(id__in=referendum_ids)

        for referendum in referendums:
            referendum.update_user_vote(self)

        # TODO: Update votes on comments

    def get_graph(self):
        """
        Creates a graph for the user based on Delegation
        """
        logger.debug("Get graph for %s" % self)
        graph = GraphEkratia()
        graph.add_user_id(self.id)
        return graph

    def get_graph_referendum(self, referendum):
        logger.debug("Get graph for %s and referendum %s" % (self, referendum))
        graph = nx.DiGraph()

        vote_user_ids = ReferendumUserVote.objects\
            .filter(referendum=referendum)\
            .exclude(user=self)\
            .values_list('user_id', flat=True)
        logger.debug("Users with votes: %s" % str(vote_user_ids))

        visited, queue = set(), [self.id]
        while queue:
            current = queue.pop(0)
            logger.debug('Current graph: %s' % current)
            logger.debug('Visited: %s' % visited)
            if current not in visited and current not in vote_user_ids:
                graph.add_node(current)
                delegates = Delegate.objects.filter(user__id=current)\
                    .exclude(delegate_id__in=vote_user_ids)
                for delegate in delegates:
                    graph.add_node(delegate.delegate.id)
                    graph.add_edge(current, delegate.delegate.id)
                    queue.append(delegate.delegate.id)

                delegated_to_me = Delegate.objects\
                    .filter(delegate__id=current)\
                    .exclude(user_id__in=vote_user_ids)
                for delegate in delegated_to_me:
                    graph.add_node(delegate.user.id)
                    graph.add_edge(delegate.user.id, current)
                    queue.append(delegate.user.id)
                visited.add(current)
            else:
                logger.debug('Skipping Visited: %s' % current)

            logger.debug('Edges: %s' % graph.edges())

        return graph

    def get_graph_value(self):
        graph = self.get_graph()
        return get_graph_value(graph, self.id)

    def get_graph_pagerank(self):
        graph = self.get_graph()
        return nx.pagerank_numpy(graph)

    def get_pagerank_value(self):
        values = self.get_graph_pagerank()
        return values[self.id] * len(values)

    # def get_pagerank_value(self):
    #     graph = self.get_graph()
    #     return 1 + graphs.count_total_predecessors(graph, self.id)

    def get_pagerank_value_referendum(self, referendum):
        graph = self.get_graph_referendum(referendum)
        pagerank_values = nx.pagerank_numpy(graph)
        return pagerank_values[self.id] * len(pagerank_values)

    # def get_pagerank_value_referendum(self, referendum):
    #     graph = self.get_graph_referendum(referendum)
    #     return 1 + graphs.count_total_predecessors(graph, self.id)

    def get_hybridrank_value(self):
        pagerank_values = self.get_graph_pagerank().values()
        return sum(pagerank_values) * (len(pagerank_values) - 1)
