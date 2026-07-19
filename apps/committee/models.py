from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.core.constants import SessionStatus, CaseStatus
from apps.patients.models import Patient
from django.core.validators import MinValueValidator, MaxValueValidator

class Doctor(models.Model):
    doctor_name = models.CharField(max_length=255, unique=True, verbose_name=_("اسم الطبيب"))

    class Meta:
        verbose_name = _("طبيب لجنة")
        verbose_name_plural = _("أطباء اللجان")
        ordering = ['doctor_name']

    def __str__(self):
        return self.doctor_name


class Procedure(models.Model):
    CATEGORY_CHOICES = [('diagnostic', _("فحوصات")), ('gamaknife', _("جاما نايف")), ('radiosurgery', _("جراحة إشعاعية"))]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='جاما نايف',
        verbose_name=_("تصنيف الإجراء الطبي")
    )
    name = models.CharField(max_length=255, unique=True, verbose_name=_("اسم الإجراء"))
    requires_referral = models.BooleanField(default=False, verbose_name=_("يتطلب تحويل لمركز خارجي"))
    price = models.CharField(
        choices= [('27000 سبعة وعشرون ألف ', _("27000")), ('28000 ثمانية وعشرون ألف', _("28000"))],
        verbose_name= _("السعر"),
        null=True,
        blank=True,
    )
    
    

    class Meta:
        verbose_name = _("إجراء طبي")
        verbose_name_plural = _("الإجراءات الطبية")
        ordering = ['category', 'name', 'price']

    def __str__(self):
        return f"{self.name}"


class CommitteeSession(models.Model):


    session_date = models.DateField(
        verbose_name=_("تاريخ الجلسة")
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name=_("الطبيب")
    )

    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.PREPARING,
        verbose_name=_("الحالة")
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_("ملاحظات")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاريخ الإنشاء")
    )

    class Meta:
        verbose_name = _("جلسة لجنة")
        verbose_name_plural = _("جلسات اللجان")
        ordering = ["-session_date", "-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["session_date"],
                name="unique_committee_session_per_day"
            )
        ]

    def __str__(self):
        return f"جلسة {self.session_date}"


class CommitteeCase(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='committee_cases', verbose_name=_("المريض"))
    committee_session = models.ForeignKey(CommitteeSession, on_delete=models.CASCADE, related_name='cases', verbose_name=_("جلسة اللجنة"))
    status = models.CharField(max_length=3, choices=CaseStatus.choices, default=CaseStatus.PENDING, verbose_name=_("حالة القرار"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("التفاصيل والتشخيص المقابل المعروض"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ العرض"))

    class Meta:
        verbose_name = _("حالة معروضة")
        verbose_name_plural = _("الحالات المعروضة باللجنة")
        ordering = ['created_at']
        unique_together = ('patient', 'committee_session')

    def __str__(self):
        return f"حالة: {self.patient.full_name} - {self.committee_session}"


class CommitteeRecommendation(models.Model):
    committee_case = models.OneToOneField(CommitteeCase, on_delete=models.CASCADE, related_name='recommendation', verbose_name=_("الحالة الطبية المعروضة"))
    procedure = models.ForeignKey(Procedure, on_delete=models.PROTECT, related_name='recommendations', verbose_name=_("الإجراء الطبي الموصى به"))
    recommendation_text = models.TextField(verbose_name=_("نص التوصية النهائي"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("ملاحظات إضافية للقرار"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ التوصية"))
    no_of_sessions = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)])

    @property
    def referral_procedure_text(self):

        if self.procedure.category == "radiosurgery":
            return f"جلسة { self.procedure } بواقع عدد {self.no_of_sessions} جلسات بعد موافقة السلطة المختصة بإدراج الخدمة بتكلفة {self.procedure.price} جنية فقط لاغير"

        else :
            return self.procedure

    class Meta:
        verbose_name = _("توصية اللجنة")
        verbose_name_plural = _("توصيات وقرارات اللجان")
        ordering = ['-created_at']

    def __str__(self):
        return f"قرار وتوصية لحالة المريض: {self.committee_case.patient.full_name}"
