import uuid
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Claim, Payment
from .serializers import (
    ClaimSerializer, PaymentSerializer, RegisterSerializer,
    UserSerializer, MyTokenObtainPairSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Claim.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        claim = serializer.save(user=self.request.user)
        # For production, consider sending emails asynchronously (e.g., with Celery)
        # to avoid blocking the API response.

        # Send email notification to user
        send_mail(
            subject='Claim Submitted',
            message=f'Your claim ({claim.claim_type}) has been submitted.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Here you would integrate with your payment provider
        # For demonstration, we mark as completed and generate a unique reference
        payment = serializer.save(
            user=self.request.user,
            status='completed',
            reference=f'PAY-{uuid.uuid4()}'
        )
        # Send payment confirmation email
        send_mail(
            subject='Payment Received',
            message=f'Your payment of {payment.amount} has been received.',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
            recipient_list=[self.request.user.email],
            fail_silently=True,
        )

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer