from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from user_accounts.views import register

router = DefaultRouter()
router.register(r'claims', views.ClaimViewSet, basename='claim')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]