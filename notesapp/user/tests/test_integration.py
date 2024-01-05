from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class UserIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_signup_and_login(self):
        signup_data = {'username': 'testuser', 'password': 'testpassword'}
        signup_response = self.client.post('http://127.0.0.1:8000/api/auth/signup/', signup_data, format='json')

        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)

        login_data = {'username': 'testuser', 'password': 'testpassword'}
        login_response = self.client.post('http://127.0.0.1:8000/api/auth/login/', login_data, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in login_response.data)
        self.assertTrue('access' in login_response.data)
