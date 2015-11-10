from django.test import TestCase, RequestFactory, Client
from ekratia.users.models import User
from ekratia.delegates.models import Delegate


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

    def test_pagerank_delegates_empty(self):
        pagerank = self.user1.compute_pagerank()
        self.assertEqual(pagerank, 1.0)

    def test_pagerank_user1_delegated_by_user2(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        pagerank1 = self.user1.compute_pagerank()
        pagerank2 = self.user2.compute_pagerank()
        pagerank3 = self.user3.compute_pagerank()
        self.assertEqual(round(pagerank1, 1), 1.3)
        self.assertEqual(round(pagerank2, 1), 0.7)
        self.assertEqual(round(pagerank3, 1), 1.0)
        self.assertEqual(pagerank1+pagerank2+pagerank3, 3)

    def test_pagerank_user1_delegated_by_user3(self):
        Delegate.objects.create(user=self.user2, delegate=self.user1)
        Delegate.objects.create(user=self.user3, delegate=self.user1)
        pagerank1 = self.user1.compute_pagerank()
        pagerank2 = self.user2.compute_pagerank()
        pagerank3 = self.user3.compute_pagerank()
        self.assertEqual(round(pagerank1, 1), 1.7)
        self.assertEqual(round(pagerank2, 1), 0.6)
        self.assertEqual(round(pagerank3, 1), 0.6)
        self.assertEqual(pagerank1+pagerank2+pagerank3, 3)
