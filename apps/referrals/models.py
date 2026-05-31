from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.core.constants import ReferralStatus
from apps.committee.models import CommitteeCase, CommitteeRecommendation

class ReferralCenter(models.Model):
    name = models.DynamicField = models.CharField(max_length=255, unique=True, verbose_name=_("اسم المركز الطبي المحال إليه"))
    address = models.CharField(max_length=500, verbose_name=_("العنوان بالكامل"))
    phone_number = models.CharField(max_length=50, verbose_name=_("أرقام التواصل للجهات الخارجية"))

    class Meta:
        verbose_name = _("مركز تحويل خارجي")
        verbose_name_plural = _("مراكز التحويل الخارجية")
        ordering = ['name']

    def __str__(self):
        return self.name


class Referral(models.Model):
    committee_case = models.ForeignKey(CommitteeCase, on_delete=models.CASCADE, related_name='referrals', verbose_name=_("حالة اللجنة الطبية"))
    referral_center = models.ForeignKey(ReferralCenter, on_delete=models.PROTECT, related_name='referrals', verbose_name=_("المركز الموجه له الحالة"))
    status = models.CharField(max_length=3, choices=ReferralStatus.choices, default=ReferralStatus.ISSUED, verbose_name=_("حالة خطاب التحويل"))
    issued_at = models.DateTimeField(default=timezone.now, verbose_name=_("تاريخ إصدار الخطاب"))
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name=_("سبب الإلغاء (إن وجد)"))

    class Meta:
        verbose_name = _("خطاب تحويل مريض")
        verbose_name_plural = _("خطابات تحويل المرضى")
        ordering = ['-issued_at']

def clean(self):
    # 1. check recommendation exists (safe DB lookup)
    if not CommitteeRecommendation.objects.filter(
        committee_case_id=self.committee_case_id
    ).exists():
        raise ValidationError(
            "يجب إصدار توصية طبية معتمدة من اللجنة للحالة أولاً قبل التمكّن من إنشاء خطاب تحويل لها."
        )

    # 2. verify procedure allows referral
    recommendation = CommitteeRecommendation.objects.get(
        committee_case_id=self.committee_case_id
    )

    if not recommendation.procedure.requires_referral:
        raise ValidationError(
            "لا يمكن إنشاء خطاب تحويل لهذه الحالة لأن الإجراء الطبي لا يتطلب تحويل."
        )

    # 3. prevent duplicate active referrals
    active_referrals = Referral.objects.filter(
        committee_case_id=self.committee_case_id
    ).exclude(status=ReferralStatus.CANCELLED)

    if self.pk:
        active_referrals = active_referrals.exclude(pk=self.pk)

    if active_referrals.exists():
        raise ValidationError(
            "توجد بالفعل إحالة أو خطاب تحويل ساري لهذه الحالة."
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"تحويل للمريض: {self.committee_case.patient.full_name} إلى {self.referral_center.name}"
# Create your models here.
