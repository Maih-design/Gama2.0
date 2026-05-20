from django import apps
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Patient, PatientDocument

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'national_id', 'full_name', 'birth_date', 'gender', 
            'phone_number', 'governorate', 'affiliated_branch', 'diagnosis'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
        }


class PatientDocumentForm(forms.ModelForm):
    class Meta:
        model = PatientDocument
        fields = ['document_type', 'file']