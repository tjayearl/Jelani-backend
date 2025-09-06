from django.contrib import admin
from .models import Claim, Payment

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'claim_type', 'status', 'created_at')
    search_fields = ('user__email', 'claim_type', 'status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')
    search_fields = ('user__email', 'status')