from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.core.constants import SessionStatus
from .models import CommitteeSession, CommitteeCase, CommitteeRecommendation, Doctor

class CommitteeSessionForm(forms.ModelForm):
    class Meta:
        model = CommitteeSession
        fields = ['session_date', 'doctor', 'status', 'notes']
        widgets = {
            'session_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status == SessionStatus.ACTIVE:
            active_sessions = CommitteeSession.objects.filter(status=SessionStatus.ACTIVE)
            if self.instance and self.instance.pk:
                active_sessions = active_sessions.exclude(pk=self.instance.pk)
            if active_sessions.exists():
                raise ValidationError(_("لا يمكن تفعيل هذه الجلسة. توجد لجنة أخرى نشطة حالياً بالنظام."))
        return status


class CommitteeCaseForm(forms.ModelForm):
    class Meta:
        model = CommitteeCase
        fields = ['patient', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class CommitteeRecommendationForm(forms.ModelForm):
    class Meta:
        model = CommitteeRecommendation
        fields = ['procedure', 'recommendation_text', 'notes']
        widgets = {
            'recommendation_text': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }