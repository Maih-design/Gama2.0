from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.core.constants import SessionStatus
from .models import CommitteeSession, CommitteeCase, CommitteeRecommendation, Doctor
from django.utils import timezone

class CommitteeSessionForm(forms.ModelForm):
    class Meta:
        model = CommitteeSession
        fields = ['session_date', 'doctor']
        widgets = {
            'session_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'frm-input'}
            ),
        }

    def clean_session_date(self):
        session_date = self.cleaned_data.get('session_date')

        existing_session = CommitteeSession.objects.filter(
            session_date=session_date
        )

        if self.instance.pk:
            existing_session = existing_session.exclude(pk=self.instance.pk)

        if existing_session.exists():
            raise ValidationError(
                "توجد لجنة مسجلة بالفعل بنفس تاريخ الانعقاد."
            )

        return session_date


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