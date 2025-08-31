from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticate user using either username or email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            # Use a Q object to query for a user where the username OR email matches.
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        # The `user_can_authenticate` check is a good practice from the default backend.
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
