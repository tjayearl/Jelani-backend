# accounts/views.py
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
import uuid

from .models import Claim, Payment
from .serializers import (
    ClaimSerializer,
    PaymentSerializer,
)

# This is a standard Django view, not a DRF one. It might be deprecated.
# Consider if you still need it.

class ClaimViewSet(viewsets.ModelViewSet):   # should allow POST
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def get_permissions(self):
        """Customize permissions depending on request method"""
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            # Viewing or managing claims → must be logged in
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Creating a claim (POST) → open to everyone
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # If logged in, show only this user's claims
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return self.queryset.none()  # hide from anonymous users

    def perform_create(self, serializer):
        # Attach user only if logged in
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class PaymentViewSet(viewsets.ModelViewSet): # should allow POST
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Generate a unique reference for the payment
        reference = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        serializer.save(user=self.request.user, reference=reference)