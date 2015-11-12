from django.test import TestCase, RequestFactory, Client

from ekratia.users.models import User

import logging
logger = logging.getLogger('ekratia')


class DelegationTestCase(TestCase):
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
        self.user2.delegate_to(self.user1)
        p1 = self.user1.get_pagerank_value()
        p2 = self.user2.get_pagerank_value()
        p3 = self.user3.get_pagerank_value()
        self.assertEqual(round(p1, 1), 1.3)
        self.assertEqual(round(p2, 1), 0.7)
        self.assertEqual(round(p3, 1), 1.0)

        self.user2.undelegate_to(self.user1)
        p1 = self.user1.get_pagerank_value()
        p2 = self.user2.get_pagerank_value()
        self.assertEqual(round(p1, 1), 1.0)
        self.assertEqual(round(p2, 1), 1.0)

    def test_pagerank_user1_delegated_by_user2_3(self):
        self.user2.delegate_to(self.user1)
        self.user3.delegate_to(self.user1)

        p1 = self.user1.get_pagerank_value()
        p2 = self.user2.get_pagerank_value()
        p3 = self.user3.get_pagerank_value()
        self.assertEqual(round(p1, 1), 1.7)
        self.assertEqual(round(p2, 1), 0.6)
        self.assertEqual(round(p3, 1), 0.6)
