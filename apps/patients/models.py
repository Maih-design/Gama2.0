from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from apps.core.constants import GenderChoices, GovernorateChoices, BranchChoices, DocumentTypeChoices, InsuranceLawChoices

# Create your models here.
# Kept clean for general extensions or abstract base classes if needed in the future

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        abstract = True



class Patient(models.Model):
    national_id = models.CharField(
        max_length=14, 
        unique=True,
        validators=[RegexValidator(r'^\d{14}$', _('الرقم القومي يجب أن يتكون من 14 رقماً.'))],
        verbose_name=_("الرقم القومي")
    )
    full_name = models.CharField(max_length=255, verbose_name=_("الاسم بالكامل"))
    birth_date = models.DateField(verbose_name=_("تاريخ الميلاد"))
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, verbose_name=_("الجنس"))
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?\d{9,15}$', _('رقم الهاتف غير صحيح.'))],
        verbose_name=_("رقم الهاتف")
    )
    governorate = models.CharField(max_length=3, choices=GovernorateChoices.choices, verbose_name=_("المحافظة"))
    affiliated_branch = models.CharField(max_length=3, choices=BranchChoices.choices, verbose_name=_("الفرع التابع له"))
    diagnosis = models.TextField(verbose_name=_("التشخيص الطبي المبدئي"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ التسجيل"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التعديل"))
    insurance_no = models.CharField(max_length=20, verbose_name=_("الرقم التأميني"))
    insurance_law = models.CharField(max_length=3, choices=InsuranceLawChoices.choices, verbose_name=_("القانون"))

    class Meta:
        verbose_name = _("مريض")
        verbose_name_plural = _("المرضى")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['full_name']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.national_id})"


def patient_directory_path(instance, filename):
    return f'patients/{instance.patient.national_id}/{filename}'

class PatientDocument(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents', verbose_name=_("المريض"))
    document_type = models.CharField(max_length=3, choices=DocumentTypeChoices.choices, verbose_name=_("نوع المستند"))
    file = models.FileField(upload_to=patient_directory_path, verbose_name=_("الملف"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الرفع"))

    class Meta:
        verbose_name = _("مستند المريض")
        verbose_name_plural = _("مستندات المرضى")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.patient.full_name}"