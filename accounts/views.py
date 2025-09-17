# accounts/views.py
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from user_accounts.serializers import RegisterSerializer
from .models import Claim, Payment
from .serializers import (
    ClaimSerializer,
    PaymentSerializer,
    CustomLoginSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_200_OK)

# This is a standard Django view, not a DRF one. It might be deprecated.
# Consider if you still need it.

class ClaimViewSet(viewsets.ModelViewSet):   # should allow POST
    permission_classes = [AllowAny]  # Temporarily allow public access for testing
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def get_queryset(self):
        return self.queryset.all() # Return all claims since it's public

    def perform_create(self, serializer):
        serializer.save() # No user to associate for anonymous submissions

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