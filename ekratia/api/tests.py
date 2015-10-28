from django.test import TestCase, RequestFactory, Client
from ekratia.users.models import User


class ApiTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        # Create sample user
        User.objects.create_user('user', 'user@email.com', 'password')
        # Authenticate Client
        self.client.login(username='user', password='password')

    def test_api_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_delegates(self):
        response = self.client.get('/api/v1/delegates/')
        self.assertEqual(response.status_code, 200)

    def test_api_delegates_available(self):
        response = self.client.get('/api/v1/delegates/available/')
        self.assertEqual(response.status_code, 200)

    def test_api_delegates_assigned(self):
        response = self.client.get('/api/v1/delegates/')
        self.assertEqual(response.status_code, 200)
