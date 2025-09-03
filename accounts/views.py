from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta

from .models import Claim, Payment, Policy, User
from .serializers import ClaimSerializer, PaymentSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view and create claims.
    """
    serializer_class = ClaimSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users should only see their own claims."""
        return Claim.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically associate the claim with the logged-in user."""
        serializer.save(user=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view and create payments.
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users should only see their own payments."""
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically associate the payment with the logged-in user."""
        serializer.save(user=self.request.user)


class LoginView(TokenObtainPairView):
    """Handles user login and returns JWT tokens."""
    # This view is referenced in your urls.py for the 'login/' path.
    # It uses the simple-jwt library to handle token generation.
    pass


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # This endpoint is public
def calculate_quote(request):
    """
    Calculate an insurance quote based on user input passed via GET query parameters.
    This is a backend-only calculation.

    Example Usage:
    /api/accounts/calculate-quote/?age=24&car_type=suv&coverage=full
    """
    # --- Get parameters from query string with defaults ---
    age_str = request.query_params.get('age', '30')
    car_type = request.query_params.get('car_type', 'sedan')
    coverage = request.query_params.get('coverage', 'basic')

    # --- Input Validation ---
    try:
        age = int(age_str)
        if age < 18:
            return Response({'error': 'Age must be 18 or older to get a quote.'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': "Parameter 'age' must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

    # --- Calculation Logic ---
    base_price = 500.0  # Start with a float for precision

    # Car type modifier
    if car_type.lower() == 'suv':
        base_price += 200
    elif car_type.lower() == 'sports':
        base_price += 400

    # Coverage modifier
    if coverage.lower() == 'full':
        base_price *= 1.5

    # Age modifier
    if age < 25:
        base_price *= 1.2

    quote = round(base_price, 2)

    # --- Prepare and return JSON response ---
    data = {'quote': quote, 'parameters': {'age': age, 'car_type': car_type, 'coverage': coverage}}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard(request):
    """
    Provides a summary for the user.
    - If the user is staff, it returns a global, admin-level overview.
    - Otherwise, it returns a business-rich summary of the user's own account.
    """
    user = request.user
    today = timezone.now().date()

    if user.is_staff:
        # --- Admin Dashboard: Global Statistics ---
        # Summary
        summary = {
            "total_policies": Policy.objects.count(),
            "total_payments": Payment.objects.count(),
            "total_claims": Claim.objects.count(),
        }

        # upcoming renewals (next 30 days)
        upcoming_renewals = (
            Policy.objects.filter(
                end_date__gte=today, end_date__lte=today + timedelta(days=30), status="active"
            )
            .select_related("user")
            .values("policy_number", "end_date", "user__username")
        )

        # Overdue renewals (expired, but still marked as active)
        overdue_renewals = (
            Policy.objects.filter(end_date__lt=today, status="active")
            .select_related("user")
            .values("policy_number", "end_date", "user__username")
        )

        # Recent activity
        recent_claims = Claim.objects.order_by("-created_at")[:5].select_related('user').values(
            "id", "policy_number", "status", "created_at", "user__username"
        )
        recent_payments = Payment.objects.order_by("-created_at")[:5].select_related('user').values(
            "id", "user__username", "amount", "created_at"
        )

        # Policy status breakdown
        status_breakdown = Policy.objects.values("status").annotate(count=Count("status"))

        return Response({
            "summary": summary,
            "upcoming_renewals": list(upcoming_renewals),
            "overdue_renewals": list(overdue_renewals),
            "recent_activity": {
                "claims": list(recent_claims),
                "payments": list(recent_payments),
            },
            "status_breakdown": list(status_breakdown),
        })

    else:
        # --- User Dashboard: Personal Statistics ---
        # Use a single aggregate query for claim stats for efficiency
        claim_summary = Claim.objects.filter(user=user).aggregate(
            claims_count=Count("id"),
            approved_claims=Count("id", filter=Q(status="approved")),
            rejected_claims=Count("id", filter=Q(status="rejected")),
        )

        # Sum of completed payments
        total_payments_agg = Payment.objects.filter(user=user, status="completed").aggregate(total=Sum("amount"))
        total_payments = total_payments_agg.get("total") or 0

        # Policy summary aggregation, using valid statuses from the Policy model
        policies_summary = Policy.objects.filter(user=user).aggregate(
            total=Count("id"),
            active=Count("id", filter=Q(status="active")),
            expired=Count("id", filter=Q(status="expired")),
            cancelled=Count("id", filter=Q(status="cancelled")),
        )

        # Upcoming renewals (active policies in the next 30 days)
        upcoming_renewals = list(
            Policy.objects.filter(user=user, status="active", end_date__range=[today, today + timedelta(days=30)])
            .values("policy_number", "end_date")
        )

        # Overdue renewals (already expired)
        overdue_renewals = list(
            Policy.objects.filter(user=user, end_date__lt=today, status="expired")
            .values("policy_number", "end_date")
        )

        # Recent activity
        recent_claims = list(
            Claim.objects.filter(user=user).order_by("-created_at")[:5]
            .values("id", "policy_number", "status", "created_at")
        )
        recent_payments = list(
            Payment.objects.filter(user=user).order_by("-created_at")[:5]
            .values("id", "amount", "status", "created_at")
        )

        return Response({
            "summary": {**claim_summary, "total_payments": total_payments, "policies": policies_summary},
            "upcoming_renewals": upcoming_renewals,
            "overdue_renewals": overdue_renewals,
            "recent_activity": {"claims": recent_claims, "payments": recent_payments},
        })
