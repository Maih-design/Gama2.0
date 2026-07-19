from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.core.constants import SessionStatus
from .models import CommitteeSession, CommitteeCase, CommitteeRecommendation, Doctor
from django.utils import timezone

class CommitteeSessionForm(forms.ModelForm):

    class Meta:
        model = CommitteeSession
        fields = ["session_date", "doctor"]

        widgets = {
            "session_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "frm-input",
                }
            ),
        }

    def clean_session_date(self):
        session_date = self.cleaned_data["session_date"]

        queryset = CommitteeSession.objects.filter(
            session_date=session_date
        )

        # في حالة تعديل جلسة موجودة
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                "تم إنشاء جلسة بالفعل في هذا التاريخ، ولا يمكن إنشاء جلستين في نفس اليوم."
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
        fields = ['procedure', 'recommendation_text', 'notes','no_of_sessions']
        widgets = {
            'recommendation_text': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }