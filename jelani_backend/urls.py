from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Simple homepage
def home(request):
    return JsonResponse({"message": "Welcome to Jelani API 🚀"})

urlpatterns = [
    # Homepage
    path('', home),

    # Admin panel
    path('admin/', admin.site.urls),

    # Auth & user accounts
    path('api/accounts/', include('accounts.urls')),       # login, register, claims, payments

    # Claims & payments (via routers in accounts app)
    # path('api/', include('accounts.urls_extra')),  # remove this for now

    # Quotes
    # path('api/quote/', include('quote.urls')),

    # Dashboard
    path('api/dashboard/', include('dashboard.urls')),

    # JWT endpoints (if not already in accounts.urls)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
