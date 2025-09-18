# accounts/views.py
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
import uuid
from rest_framework.permissions import IsAuthenticated

from .models import Claim, Payment
from .serializers import (
    ClaimSerializer,
    PaymentSerializer,
)

# This is a standard Django view, not a DRF one. It might be deprecated.
# Consider if you still need it.

class ClaimViewSet(viewsets.ModelViewSet):   # should allow POST
    permission_classes = [IsAuthenticated]
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet): # should allow POST
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Generate a unique reference for the payment
        reference = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        serializer.save(user=self.request.user, reference=reference)