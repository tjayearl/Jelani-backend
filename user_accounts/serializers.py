from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="An account with this email already exists.")]
    )
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        # We expect these from the frontend, and will derive the model fields.
        fields = ['full_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match."})
        
        # Run Django's built-in password validators
        validate_password(attrs['password'])

        # Check for existing username (derived from email)
        # This prevents IntegrityError at the database level if two emails
        # (e.g., 'user@gmail.com' and 'user@yahoo.com') produce the same username.
        username = attrs['email'].split('@')[0]
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": f"The username '{username}' is already taken. Please choose a different email."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        full_name = validated_data['full_name']
        first_name, *last_name_parts = full_name.split(' ', 1)
        last_name = last_name_parts[0] if last_name_parts else ''

        # Create a username from the email prefix
        username = validated_data['email'].split('@')[0]

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    Handles user login, allowing authentication with either username or email.
    Returns JWT refresh and access tokens.
    """
    login = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        login = data.get("login")
        password = data.get("password")

        # First, try authenticating with the login field as a username
        user = authenticate(username=login, password=password)

        # If that fails, try treating the login field as an email
        if not user:
            try:
                user_obj = User.objects.get(email=login)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass  # The final check below will handle the failure

        if not user:
            raise AuthenticationFailed("Invalid login credentials.")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
            }
        }