from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from user_accounts.views import LoginView, RegisterView

router = DefaultRouter()
router.register(r'claims', views.ClaimViewSet, basename='claim')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='custom_login'),
    path('register/', RegisterView.as_view(), name='custom_register'),
]