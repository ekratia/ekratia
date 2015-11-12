from django.test import TestCase, RequestFactory, Client
from django.utils import timezone

from ekratia.users.models import User
from ekratia.delegates.models import Delegate
from ekratia.referendums.models import Referendum, ReferendumUserVote

import logging
logger = logging.getLogger('ekratia')


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

    def test_process_vote(self):
        vote, created = self.referendum.vote_process(self.user1, 1)
        self.assertIsInstance(vote, ReferendumUserVote)
        with self.assertRaises(ValueError):
            vote = self.referendum.vote_process(self.user1, 100)

    def test_pagerank_delegates_empty(self):
        pagerank = self.user1.get_pagerank_value()
        self.assertEqual(pagerank, 1.0)

    def test_delegate_create_delete(self):
        self.user2.delegate_to(self.user1)
        p1 = self.user1.get_pagerank_value()
        self.assertEqual(round(p1, 1), 1.3)
        self.user2.undelegate_to(self.user1)
        p1 = self.user1.get_pagerank_value()
        self.assertEqual(round(p1, 1), 1.0)

    def test_pagerank_user1_delegated_by_user2(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        p1 = self.user1.get_pagerank_value()
        p2 = self.user2.get_pagerank_value()
        p3 = self.user3.get_pagerank_value()
        self.assertEqual(round(p1, 1), 1.3)
        self.assertEqual(round(p2, 1), 0.7)
        self.assertEqual(round(p3, 1), 1.0)

    def test_pagerank_user1_delegated_by_user2_3(self):
        self.user2.delegate_to(self.user1)
        self.user3.delegate_to(self.user1)

        p1 = self.user1.get_pagerank_value()
        p2 = self.user2.get_pagerank_value()
        p3 = self.user3.get_pagerank_value()
        self.assertEqual(round(p1, 1), 1.7)
        self.assertEqual(round(p2, 1), 0.6)
        self.assertEqual(round(p3, 1), 0.6)

    def setup_votes_scenario1(self):
        self.referendum.vote_process(self.user1, 1)
        self.referendum.vote_process(self.user2, -1)
        self.referendum.vote_process(self.user3, 1)

    def setup_delegates_scenario1(self):
        self.user2.delegate_to(self.user1)
        self.user3.delegate_to(self.user1)
        # logger.debug("user1 pagerank: %s" % self.user1.get_pagerank_value())

    def test_referendum_count_votes(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        self.assertEqual(self.referendum.get_count_votes(), 3)

    def test_referendum_calculate_votes(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        logger.debug("DELEGATE 1: %s" % self.user1.get_pagerank_value())
        self.assertEqual(self.referendum.calculate_votes(), 1)

    def test_referendum_num_positive_votes(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        self.assertEqual(self.referendum.get_num_positive_votes(), 2)

    def test_referendum_num_negative_votes(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        self.assertEqual(self.referendum.get_num_negative_votes(), 1)

    def test_referendum_total_votes_absolute(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        self.assertEqual(self.referendum.get_total_votes_absolute(), 3)


# get_total_votes_absolute
class ReferendumsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        # Create sample user
        User.objects.create_user('user', 'user@email.com', 'password')
        # Authenticate Client
        self.client.login(username='user', password='password')

    def test_url(self):
        response = self.client.get('/referendums/')
        self.assertEqual(response.status_code, 200)

    def test_url_create(self):
        response = self.client.get('/referendums/create')
        self.assertEqual(response.status_code, 200)
