# accounts/views.py
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Claim, Payment
from .serializers import ClaimSerializer, PaymentSerializer

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

class LoginView(APIView):
    def post(self, request):
        # The custom backend allows 'username' to be either a username or an email
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)