from django.test import TestCase, RequestFactory, Client
from ekratia.users.models import User
from ekratia.users.models import Delegate

import networkx as nx
import logging
logger = logging.getLogger('ekratia')


class UserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        # Create sample user
        self.user1 = User.objects.create_user(
            'user1', 'user1@email.com', 'password')
        self.user2 = User.objects.create_user(
            'user2', 'user2@email.com', 'password')
        self.user2.first_name = 'Andres'
        self.user2.last_name = 'Gonzalez'
        self.user2.save()

    def test_avatar(self):
        self.assertEqual(
            self.user1.get_avatar, u'http://placehold.it/75x75/')

    def test_get_full_name_or_username(self):
        self.assertEqual(self.user1.get_full_name_or_username, 'user1')
        self.assertEqual(
            self.user2.get_full_name_or_username, 'Andres Gonzalez')

    def test_delegate_user(self):
        delegate = self.user1.delegate_to(self.user2)
        self.assertIsInstance(delegate, Delegate)

    def test_undelegate_user(self):
        self.user1.delegate_to(self.user2)
        result = self.user1.undelegate_to(self.user2)
        self.assertTrue(result)
        self.assertFalse(Delegate.objects.filter(user=self.user1).exists())


class UserGraphTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            'user1', 'user@email.com', 'password')
        self.user2 = User.objects.create_user(
            'user2', 'user@email.com', 'password')
        self.user3 = User.objects.create_user(
            'user3', 'user@email.com', 'password')
        self.user4 = User.objects.create_user(
            'user4', 'user@email.com', 'password')
        self.user5 = User.objects.create_user(
            'user5', 'user@email.com', 'password')

    def setup_delegation1(self):
        # All the users delegate user1
        self.user2.delegate_to(self.user1)
        self.user3.delegate_to(self.user1)
        self.user3.delegate_to(self.user1)
        self.user4.delegate_to(self.user1)

    def setup_delegation2(self):
        # 3 to 1
        # 4 to 1,2
        self.user3.delegate_to(self.user1)
        self.user4.delegate_to(self.user1)
        self.user4.delegate_to(self.user2)

    def setup_delegation3(self):
        self.user3.delegate_to(self.user1)
        self.user4.delegate_to(self.user1)
        self.user4.delegate_to(self.user2)
        self.user5.delegate_to(self.user4)

    def setup_delegation4(self):
        # Circular delegation
        self.user3.delegate_to(self.user1)
        self.user4.delegate_to(self.user1)
        self.user4.delegate_to(self.user2)
        self.user1.delegate_to(self.user4)

    def test_get_graph(self):
        self.setup_delegation1()
        graph = self.user1.get_graph()
        self.assertIsInstance(graph, nx.DiGraph)

    def test_get_graph_value_delegation1(self):
        self.setup_delegation1()
        self.assertEqual(self.user1.get_graph_value(), 4.0)

    def test_get_graph_value_delegation2(self):
        self.setup_delegation2()
        self.assertEqual(self.user1.get_graph_value(), 2.5)
        self.assertEqual(self.user2.get_graph_value(), 1.5)
        self.assertEqual(self.user3.get_graph_value(), 1.0)
        self.assertEqual(self.user4.get_graph_value(), 1.0)

    def test_get_graph_value_delegation3(self):
        self.setup_delegation3()
        self.assertIsInstance(self.user1.get_graph(), nx.DiGraph)
        self.assertEqual(self.user1.get_graph_value(), 3.0)
        self.assertEqual(self.user2.get_graph_value(), 2.0)
        self.assertEqual(self.user3.get_graph_value(), 1.0)
        self.assertEqual(self.user4.get_graph_value(), 2.0)
        self.assertEqual(self.user5.get_graph_value(), 1.0)

    def test_get_graph_value_delegation4(self):
        self.setup_delegation4()
        self.assertIsInstance(self.user1.get_graph(), nx.DiGraph)
        # Circular dependency
