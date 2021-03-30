from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the user API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test Creating with valic payload is successful"""
        payload = {
            'email': 'test@hamza.com',
            'password': 'testPassword',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists"""
        payload = {
            'email': 'test@hamza.com',
            'password': 'testPassword'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test creating user with too short password"""
        payload = {
            'email': 'test@hamza.com',
            'password': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exits = get_user_model().objects.filters(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exits)