from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

from .models import Claim, Payment
User = get_user_model()

class CustomLoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login_value = data.get("login")
        password = data.get("password")

        # Try to authenticate by username first
        user = authenticate(username=login_value, password=password)

        if not user:
            # Try authenticating by email
            try:
                user_obj = User.objects.get(email=login_value)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if not user:
            raise serializers.ValidationError("Invalid username/email or password.")

        data["user"] = user
        return data

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"
        read_only_fields = ('user', 'status') # User is set from request, status is managed internally

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ('user', 'status', 'reference') # These are set by the server