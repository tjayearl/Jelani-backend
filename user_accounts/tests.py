from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthTests(APITestCase):
    """
    Test suite for user registration and login endpoints in the 'accounts' app.
    """

    def setUp(self):
        """
        Set up test data for the tests.
        """
        self.register_url = reverse('custom_register')
        self.login_url = reverse('custom_login')

        self.user_data = {
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "StrongPassword123!",
            "password2": "StrongPassword123!"
        }
        # The username that should be created by the serializer
        self.expected_username = "testuser"

    def test_successful_registration(self):
        """
        Ensure a user can be registered successfully.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the user was created in the database
        self.assertTrue(User.objects.filter(username=self.expected_username).exists())
        user = User.objects.get(username=self.expected_username)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_registration_with_mismatched_passwords(self):
        """
        Ensure registration fails if passwords do not match.
        """
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = "WrongPassword"
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "Password fields do not match.")

    def test_registration_with_existing_email(self):
        """
        Ensure registration fails if the email is already in use.
        """
        # Create a user first
        self.client.post(self.register_url, self.user_data, format='json')

        # Attempt to register again with the same email
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_successful_login_with_email(self):
        """
        Ensure a registered user can log in using their email.
        """
        # First, register the user
        self.client.post(self.register_url, self.user_data, format='json')

        login_data = {
            "login": self.user_data['email'],
            "password": self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])

    def test_successful_login_with_username(self):
        """
        Ensure a registered user can log in using their username.
        """
        self.client.post(self.register_url, self.user_data, format='json')

        login_data = {
            "login": self.expected_username,
            "password": self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], self.expected_username)
