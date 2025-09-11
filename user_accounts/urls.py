from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('login/', obtain_auth_token, name='user-login'),
]