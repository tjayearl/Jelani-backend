from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # Also include Django's built-in authentication views.
    # This keeps all template-based auth URLs together.
    path('', include('django.contrib.auth.urls')),
]