from django.contrib import admin
from .models import Doctor, Procedure, CommitteeSession, CommitteeCase, CommitteeRecommendation

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name',)
    search_fields = ('doctor_name',)

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'requires_referral')
    list_filter = ('category', 'requires_referral')
    search_fields = ('name',)

class CommitteeCaseInline(admin.StackedInline):
    model = CommitteeCase
    extra = 1

@admin.register(CommitteeSession)
class CommitteeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_date', 'doctor', 'status', 'created_at')
    list_filter = ('status', 'session_date', 'doctor')
    search_fields = ('notes', 'doctor__doctor_name')
    inlines = [CommitteeCaseInline]
    date_hierarchy = 'session_date'

class CommitteeRecommendationInline(admin.StackedInline):
    model = CommitteeRecommendation
    extra = 1

@admin.register(CommitteeCase)
class CommitteeCaseAdmin(admin.ModelAdmin):
    list_display = ('patient', 'committee_session', 'status', 'created_at')
    list_filter = ('status', 'committee_session__session_date')
    search_fields = ('patient__full_name', 'patient__national_id', 'notes')
    inlines = [CommitteeRecommendationInline]

@admin.register(CommitteeRecommendation)
class CommitteeRecommendationAdmin(admin.ModelAdmin):
    list_display = ('committee_case', 'procedure', 'created_at')
    list_filter = ('procedure__category', 'created_at')
    search_fields = ('committee_case__patient__full_name', 'recommendation_text')