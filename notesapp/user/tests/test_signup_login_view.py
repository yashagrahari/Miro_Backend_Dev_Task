from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSignUpLoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_signup_success(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('http://127.0.0.1:8000/api/auth/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'],data['username'])

    def test_user_signup_missing_data(self):
        data = {'password': 'testpassword'}
        response = self.client.post('http://127.0.0.1:8000/api/auth/signup/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in response.data)

    def test_user_login_success(self):
        user = User.objects.create_user(username='testuser', password='testpassword')

        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('http://127.0.0.1:8000/api/auth/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)

    def test_user_login_invalid_credentials(self):
        data = {'username': 'nonexistentuser', 'password': 'invalidpassword'}
        response = self.client.post('http://127.0.0.1:8000/api/auth/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
