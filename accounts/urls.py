from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    ProfileView,
    MyTokenObtainPairView,
    ClaimViewSet,
    PaymentViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'claims', ClaimViewSet, basename='claim')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]
