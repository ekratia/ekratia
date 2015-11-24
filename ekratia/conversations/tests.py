from django.test import TestCase, RequestFactory, Client
from ekratia.users.models import User


class ConversationsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        # Create sample user
        User.objects.create_user('user', 'user@email.com', 'password')
        # Authenticate Client
        self.client.login(username='user', password='password')

    def test_url(self):
        response = self.client.get('/en/conversations/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/es/conversations/')
        self.assertEqual(response.status_code, 200)

    def test_url_create(self):
        response = self.client.get('/en/conversations/create')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/es/conversations/create')
        self.assertEqual(response.status_code, 200)
