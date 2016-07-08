from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import activate

from ekratia.users.models import User
from ekratia.referendums.models import Referendum

import logging
logger = logging.getLogger('ekratia')


class ReferendumViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        # Create sample user
        User.objects.create_user('user', 'user@email.com', 'password')
        # Authenticate Client
        self.client.login(username='user', password='password')
        self.user1 = User.objects.create_user(
            'user1', 'user@email.com', 'password')
        self.user2 = User.objects.create_user(
            'user2', 'user@email.com', 'password')
        self.user3 = User.objects.create_user(
            'user3', 'user@email.com', 'password')

        self.referendum1 = Referendum.objects.create(
            text_add_rules='add rules',
            text_remove_rules='remove rules',
            user=self.user1,
            )

        self.referendum2 = Referendum.objects.create(
            text_add_rules='add rules 2',
            text_remove_rules='remove rules 2',
            user=self.user2,
            open_time=timezone.now()
            )

        self.referendum3 = Referendum.objects.create(
            text_add_rules='add rules 3',
            text_remove_rules='remove rules 3',
            user=self.user3,
            )
        self.referendum1.save()
        self.referendum2.save()
        self.referendum3.save()
        activate('en')

    def test_list_referendums(self):
        response = self.client.get(reverse('referendums:list'))
        self.assertEqual(response.status_code, 200)
        referendums_open = response.context[-1]['referendums_open']
        referendums_created = response.context[-1]['referendums_created']
        self.assertEqual(len(referendums_open),
                         Referendum.objects.open().count())
        self.assertEqual(len(referendums_created),
                         Referendum.objects.created().count())

    def test_list_referendums_order(self):
        response = self.client.get(reverse('referendums:list'))
        referendums_created = response.context[-1]['referendums_created']
        self.assertEqual(referendums_created[0], self.referendum3)
        self.assertEqual(referendums_created[1], self.referendum1)


class ReferendumVoteTestCase(TestCase):
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
        self.user4 = User.objects.create_user(
            'user4', 'user@email.com', 'password')

        self.referendum = Referendum.objects.create(
            text_add_rules='add rules',
            text_remove_rules='remove rules',
            user=self.user1,
            open_time=timezone.now()
            )

    def setup_votes_scenario1(self):
        self.referendum.vote_process(self.user1, 1)
        self.referendum.vote_process(self.user3, 1)
        self.referendum.vote_process(self.user2, -1)

    def setup_votes_scenario2(self):
        self.referendum.vote_process(self.user1, 1)
        self.referendum.vote_process(self.user2, -1)

    def setup_votes_scenario3(self):
        self.referendum.vote_process(self.user1, 1)

    def setup_delegates_scenario1(self):
        self.user2.delegate_to(self.user1)
        self.user3.delegate_to(self.user1)

    def test_referendum_vote_value_scenario1_0(self):
        # Delegation 1 - No votes
        self.setup_delegates_scenario1()
        # Vote values
        user1_vote_value = self.user1\
            .vote_count_for_referendum(self.referendum)
        user2_vote_value = self.user2\
            .vote_count_for_referendum(self.referendum)
        user3_vote_value = self.user3\
            .vote_count_for_referendum(self.referendum)

        self.assertEqual(round(user1_vote_value, 1), 1.7)
        self.assertEqual(round(user2_vote_value, 1), 0.6)
        self.assertEqual(round(user3_vote_value, 1), 0.6)

    def test_referendum_vote_value_scenario1_1(self):
        # Delegation 1 - Votes 1
        self.setup_delegates_scenario1()
        self.setup_votes_scenario1()
        # Vote values
        user1_vote_value = self.user1\
            .vote_count_for_referendum(self.referendum)
        user2_vote_value = self.user2\
            .vote_count_for_referendum(self.referendum)
        user3_vote_value = self.user3\
            .vote_count_for_referendum(self.referendum)

        self.assertEqual(user1_vote_value, 1.0)
        self.assertEqual(user2_vote_value, 1.0)
        self.assertEqual(user3_vote_value, 1.0)

    def test_referendum_vote_value_scenario1_2(self):
        # Delegation 1 - Vote 1
        self.setup_delegates_scenario1()
        self.setup_votes_scenario1()
        # Vote values
        user1_vote_value = self.user1\
            .vote_count_for_referendum(self.referendum)
        user2_vote_value = self.user2\
            .vote_count_for_referendum(self.referendum)
        user3_vote_value = self.user3\
            .vote_count_for_referendum(self.referendum)

        self.assertEqual(user1_vote_value, 1.0)
        self.assertEqual(user2_vote_value, 1.0)
        self.assertEqual(user3_vote_value, 1.0)

    def test_referendum_count_votes(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        self.assertEqual(self.referendum.get_count_votes(), 3)

    def test_referendum_calculate_votes(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        logger.debug("DELEGATE 1: %s" % self.user1.get_pagerank_value())
        self.assertEqual(self.referendum.calculate_votes(), 3.0)

    def test_referendum_num_positive_votes(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        self.assertEqual(self.referendum.get_num_positive_votes(), 3.0)

    def test_referendum_num_negative_votes(self):
        self.setup_delegates_scenario1()
        self.setup_votes_scenario1()
        self.assertEqual(self.referendum.get_num_negative_votes(), 1.0)

    def test_referendum_total_votes_absolute(self):
        self.setup_votes_scenario1()
        self.setup_delegates_scenario1()
        self.assertEqual(self.referendum.get_total_votes_absolute(), 3.0)

    def setup_delegates_scenario2(self):
        self.user2.delegate_to(self.user1)
        self.user3.delegate_to(self.user1)
