from django.contrib import admin
from .models import Patient, PatientDocument

class PatientDocumentInline(admin.TabularInline):
    model = PatientDocument
    extra = 1

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('national_id', 'full_name', 'birth_date', 'gender', 'governorate', 'affiliated_branch', 'created_at')
    list_filter = ('gender', 'governorate', 'affiliated_branch')
    search_fields = ('national_id', 'full_name', 'phone_number')
    inlines = [PatientDocumentInline]
    date_hierarchy = 'created_at'

@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'document_type', 'created_at')
    list_filter = ('document_type',)
    search_fields = ('patient__full_name', 'patient__national_id')
