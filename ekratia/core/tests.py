from django.test import TestCase, RequestFactory, Client
from ekratia.users.models import User
from ekratia.delegates.models import Delegate
from ekratia.referendums.models import Referendum, ReferendumUserVote
from django.utils import timezone

import time


class PagerankTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        # Create sample user
        self.user1 = User.objects.create_user(
            'user1', 'user@email.com', 'password')
        self.user2 = User.objects.create_user(
            'user2', 'user@email.com', 'password')
        self.user3 = User.objects.create_user(
            'user3', 'user@email.com', 'password')

        self.referendum = Referendum.objects.create(
            text_add_rules='add rules',
            text_remove_rules='remove rules',
            user=self.user1,
            open_time=timezone.now()
            )

    def referendum_user_vote(self, user, value):
        ReferendumUserVote.objects.create(
            referendum=self.referendum,
            user=user,
            value=user.get_pagerank()*value
            )

    def update_user(self, user):
        return User.objects.get(pk=user.id)

    def test_pagerank_delegates_empty(self):
        pagerank = self.user1.compute_pagerank()
        self.assertEqual(pagerank, 1.0)

    def test_delegate_create_delete(self):
        d1 = Delegate.objects.create(user=self.user2, delegate=self.user1)
        p1 = self.user1.get_pagerank()
        self.assertEqual(round(p1, 1), 1.3)
        d1.delete()
        p1 = self.user1.get_pagerank()
        self.assertEqual(round(p1, 1), 1.0)

    def test_pagerank_user1_delegated_by_user2(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        p1 = self.user1.get_pagerank()
        p2 = self.user2.get_pagerank()
        p3 = self.user3.get_pagerank()
        self.assertEqual(round(p1, 1), 1.3)
        self.assertEqual(round(p2, 1), 1.0)
        self.assertEqual(round(p3, 1), 1.0)

    def test_pagerank_user1_delegated_by_user2_3(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        Delegate.objects.create(user=self.user3, delegate=self.user1)
        p1 = self.user1.get_pagerank()
        p2 = self.user2.get_pagerank()
        p3 = self.user3.get_pagerank()
        self.assertEqual(round(p1, 1), 1.7)
        self.assertEqual(round(p2, 1), 1.0)
        self.assertEqual(round(p3, 1), 1.0)

    def test_pagerank_user2_delegated_by_user2_3_n_2_by_3(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        Delegate.objects.create(user=self.user3, delegate=self.user1)
        Delegate.objects.create(user=self.user3, delegate=self.user2)
        p1 = self.user1.compute_pagerank()
        p2 = self.user2.compute_pagerank()
        p3 = self.user3.compute_pagerank()
        self.assertEqual(round(p1, 1), 1.6)
        self.assertEqual(round(p2, 1), 1.3)
        self.assertEqual(round(p3, 1), 1.0)

    def test_referendum_user_vote_no_delegation(self):
        self.referendum_user_vote(self.user1, 1)
        self.referendum = self.referendum.update_totals()
        self.assertEqual(self.referendum.total_votes, 1)
        self.assertEqual(self.referendum.total_yes, 1.0)
        self.assertEqual(self.referendum.total_no, 0)
        self.referendum_user_vote(self.user2, 1)
        self.referendum = self.referendum.update_totals()
        self.assertEqual(self.referendum.total_votes, 2)
        self.assertEqual(self.referendum.total_yes, 2.0)
        self.assertEqual(self.referendum.total_no, 0)
        self.referendum_user_vote(self.user3, -1)
        self.referendum = self.referendum.update_totals()
        self.assertEqual(self.referendum.total_votes, 3)
        self.assertEqual(self.referendum.total_yes, 2.0)
        self.assertEqual(self.referendum.total_no, 1.0)

    def test_referendum_user_vote_user1_delegated_by_user2(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        self.referendum_user_vote(self.user1, 1)
        self.referendum = self.referendum.update_totals()
        self.assertEqual(round(self.referendum.total_votes, 1), 1.3)
        self.assertEqual(round(self.referendum.total_yes, 1), 1.3)
        self.assertEqual(self.referendum.total_no, 0)
        self.assertEqual(round(self.referendum.points, 1), 1.3)
        self.referendum_user_vote(self.user2, 1)
        self.assertEqual(
            self.user1.vote_count_for_referendum(self.referendum), 1.0)
        self.assertEqual(
            round(self.user2.vote_count_for_referendum(self.referendum), 1),
            1.0)

    def test_referendum_user_vote_user1_delegated_by_user2_user3(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        Delegate.objects.create(user=self.user3, delegate=self.user1)
        # user1 vote value
        self.assertEqual(
            round(self.user1.vote_count_for_referendum(self.referendum), 1),
            1.7)
        # User2 votes
        self.referendum_user_vote(self.user2, 1)
        self.assertEqual(
            round(self.user1.vote_count_for_referendum(self.referendum), 1),
            1.3)

        self.referendum_user_vote(self.user3, 1)
        self.assertEqual(
            round(self.user2.vote_count_for_referendum(self.referendum), 1),
            1.0)
