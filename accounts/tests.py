from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Claim, Payment

User = get_user_model()

class ClaimTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        # Obtain JWT token
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        # Set credentials for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_claim(self):
        url = reverse('claim-list')
        data = {'claim_type': 'Accident', 'description': 'Test claim'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify the claim was created and assigned to the correct user
        self.assertEqual(Claim.objects.count(), 1)
        self.assertEqual(Claim.objects.get().user, self.user)

class PaymentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='payuser', email='pay@example.com', password='testpass')
        # Obtain JWT token
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username': 'payuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        # Set credentials for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_payment(self):
        url = reverse('payment-list')
        data = {'amount': '100.00'} 
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.get()
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount, 100.00)
        self.assertTrue(payment.reference.startswith('PAY-'))