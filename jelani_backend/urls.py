from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

# Simple homepage
def home(request):
    return JsonResponse({"message": "Welcome to Jelani API 🚀"})

urlpatterns = [
    # Homepage
    path('', home),

    # Admin panel
    path('admin/', admin.site.urls),

    # Auth
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Dashboard
    path('api/dashboard/', include('dashboard.urls')),

    # User Accounts specific endpoints
    path('api/user/', include('user_accounts.urls')),

    # Other app endpoints (claims, payments)
    path('api/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
