# accounts/views.py
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# This is a standard Django view, not a DRF one. It might be deprecated.
# Consider if you still need it.
def payment_view(request):
    # Integrate payment logic here
    pass

def calculate_quote(request):
    return JsonResponse({"message": "Quote calculation placeholder"})

def dashboard(request):
    return JsonResponse({"message": "Dashboard placeholder"})

class ClaimViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "Claim list placeholder"})

class PaymentViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "Payment list placeholder"})

class LoginView(APIView):
    def post(self, request):
        # The custom backend allows 'username' to be either a username or an email
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)