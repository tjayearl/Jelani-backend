# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Claim, Payment, Policy

User = get_user_model()

# Optional: show Claim and Payment inline on the User admin page
class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0
    fields = ("claim_type", "status", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ("amount", "status", "transaction_id", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True

class PolicyInline(admin.TabularInline):
    model = Policy
    extra = 0
    fields = ("policy_number", "policy_type", "status", "end_date")
    readonly_fields = ("policy_number",)
    show_change_link = True


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    model = User
    # Add phone_number to list_display and search_fields
    list_display = ("id", "username", "email", "phone_number", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "phone_number")

    # To make custom fields editable, they must be added to the fieldsets.
    # This adds a new section 'Extra Info' to the user change page.
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number',)}),
    )
    # This also adds the phone_number field to the user creation page.
    add_fieldsets = DefaultUserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

    # Keep the rest of the original configuration
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("id",)
    inlines = (ClaimInline, PaymentInline, PolicyInline)


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "policy_number", "claim_type", "claim_amount", "status", "date_of_incident", "created_at")
    list_filter = ("status", "claim_type")
    search_fields = ("user__username", "user__email", "policy_number", "claim_type")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    fields = ("user", "policy_number", "claim_type", "description", "date_of_incident", "claim_amount", "document", "status")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "policy", "amount", "transaction_id", "method", "status", "created_at")
    list_filter = ("status", "method", "created_at")
    search_fields = ("transaction_id", "user__username", "policy__policy_number")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    fields = ("user", "policy", "amount", "method", "status", "transaction_id")


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "policy_number", "policy_type", "status", "premium", "start_date", "end_date")
    list_filter = ("status", "policy_type")
    search_fields = ("user__username", "user__email", "policy_number")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    fields = ("user", "policy_number", "policy_type", "premium", "start_date", "end_date", "status")