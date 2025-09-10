# accounts/views.py
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

from .models import Claim, Payment
from .serializers import ClaimSerializer, PaymentSerializer

User = get_user_model()

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

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The frontend sends 'username' which can be a username or an email
        login_identifier = attrs.get(self.username_field)
        password = attrs.get("password")

        user = None

        # First, try to authenticate with the identifier as a username
        user = authenticate(username=login_identifier, password=password)

        # If that fails, try to authenticate with it as an email
        if not user:
            try:
                user_obj = User.objects.get(email=login_identifier)
                # Authenticate with the found user's actual username
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass # User with this email does not exist

        if not user or not user.is_active:
            raise AuthenticationFailed("No active account found with the given credentials")

        # If we got here, user is valid.
        # We need to call the parent's validate method to get the token.
        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer