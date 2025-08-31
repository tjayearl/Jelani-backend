from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Claim, Payment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'policy_number')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'policy_number')}),
    )
    list_display = ('username', 'email', 'phone_number', 'policy_number', 'is_staff')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'claim_type', 'status', 'created_at')
    list_filter = ('status', 'claim_type')
    search_fields = ('user__email', 'user__username', 'claim_type')
    readonly_fields = ('created_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'reference', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'user__username', 'reference')
    readonly_fields = ('created_at', 'reference')