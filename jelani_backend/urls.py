from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Simple homepage
def home(request):
    return JsonResponse({"message": "Welcome to Jelani API 🚀"})

urlpatterns = [
    # Homepage
    path('', home),

    # Admin panel
    path('admin/', admin.site.urls),

    # Auth & user accounts
    path('api/accounts/', include('accounts.urls')),       # login, register, JWT
    path('api/accounts/', include('user_accounts.urls')),  # if you have a separate user_accounts app

    # Claims & payments (via routers in accounts app)
    path('api/', include('accounts.urls_extra')),  # 👈 we’ll put claims & payments here

    # Quotes
    path('api/quote/', include('quote.urls')),

    # Dashboard
    path('api/dashboard/', include('dashboard.urls')),

    # JWT endpoints (if not already in accounts.urls)
    path('api/token/', include('rest_framework_simplejwt.urls')),
]
