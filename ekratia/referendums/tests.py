from django.test import TestCase, RequestFactory, Client
from ekratia.users.models import User


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
