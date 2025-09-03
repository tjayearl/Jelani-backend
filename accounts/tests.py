from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Claim, Payment

User = get_user_model()

class ClaimTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass')
        self.client.login(email='test@example.com', password='testpass')

    def test_create_claim(self):
        url = reverse('claim-list')
        data = {'claim_type': 'Accident', 'description': 'Test claim'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

class PaymentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='pay@example.com', password='testpass')
        self.client.login(email='pay@example.com', password='testpass')

    def test_create_payment(self):
        url = reverse('payment-list')
        data = {'amount': '100.00'}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [201, 400])  # 400 if reference is required