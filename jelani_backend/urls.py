from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from accounts.views import calculate_quote, dashboard
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home(request):
    return JsonResponse({"message": "Welcome to Jelani API 🚀"})

urlpatterns = [
    path('', home, name='home'), # Homepage route
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    # Standalone API endpoint for quote calculation
    path('api/quote/', calculate_quote, name='calculate_quote'),
    # Standalone API endpoint for the dashboard
    path('api/dashboard/', dashboard, name='dashboard'),

    # JWT authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Includes registration, login, logout, password reset, etc.
    # from user_accounts.urls and django.contrib.auth.urls
    path('accounts/', include('user_accounts.urls')),
]
