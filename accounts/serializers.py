from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Claim, Payment

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True) # Assuming phone is not on the default User model
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["full_name", "email", "phone", "password"]

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        # Note: 'phone' is not a standard field on Django's User model.
        # It will be in validated_data but ignored by create_user unless you have a custom user model.
        validated_data.pop("phone", None)

        first_name, *last_name_parts = full_name.split(" ", 1)
        last_name = last_name_parts[0] if last_name_parts else ""

        email = validated_data["email"]
        username = email.split("@")[0]  # auto-username from email

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=validated_data["password"]
        )

        return user

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at', 'reference')

class CustomLoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

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
                pass # The final check below will handle the failure

        if not user:
            raise AuthenticationFailed("Invalid login credentials")

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