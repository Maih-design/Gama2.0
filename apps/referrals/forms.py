from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Referral

class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['referral_center']


class CancelReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['cancellation_reason']
        widgets = {
            'cancellation_reason': forms.Textarea(attrs={'rows': 3, 'required': 'required'}),
        }