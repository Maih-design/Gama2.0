from django.contrib import admin
from .models import ReferralCenter, Referral

@admin.register(ReferralCenter)
class ReferralCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')
    search_fields = ('name', 'phone_number')

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('committee_case', 'referral_center', 'status', 'issued_at')
    list_filter = ('status', 'issued_at', 'referral_center')
    search_fields = ('committee_case__patient__full_name', 'cancellation_reason')
    date_hierarchy = 'issued_at'