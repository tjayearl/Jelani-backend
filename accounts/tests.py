from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Claim, Payment

User = get_user_model()

class AuthAndUserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')

    def _get_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_registration(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'new@example.com', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_create_claim(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('claim-list')
        data = {'claim_type': 'Accident', 'description': 'Test claim'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Claim.objects.count(), 1)
        self.assertEqual(Claim.objects.get().user, self.user)

    def test_create_payment(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('payment-list')
        data = {'amount': '100.00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.get()
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.status, 'completed')