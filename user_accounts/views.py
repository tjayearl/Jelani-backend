from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """Handles user registration."""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
