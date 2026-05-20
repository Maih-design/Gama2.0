from django.db import models
from django.utils.translation import gettext_lazy as _

class GenderChoices(models.TextChoices):
    MALE = 'M', _('ذكر')
    FEMALE = 'F', _('أنثى')

class GovernorateChoices(models.TextChoices):
    CAIRO = 'CAI', _('القاهرة')
    ALEXANDRIA = 'ALX', _('الإسكندرية')
    GIZA = 'GIZ', _('الجيزة')
    QALYUBIA = 'QLY', _('القليوبية')
    PORT_SAID = 'PSD', _('بورسعيد')
    SUEZ = 'SUZ', _('السويس')
    GHARBIA = 'GHR', _('الغربية')
    DUQI = 'DKH', _('الدقهلية')
    ASWAN = 'ASW', _('أسوان')
    LUXOR = 'LUX', _('الأقصر')
    # Expandable as required by the business region

class BranchChoices(models.TextChoices):
    MAIN = 'HQ', _('الفرع الرئيسي')
    NORTH = 'NTH', _('فرع الوجه البحري')
    SOUTH = 'STH', _('فرع الوجه القبلي')

class SessionStatus(models.TextChoices):
    SCHEDULED = 'SCH', _('مجدولة')
    ACTIVE = 'ACT', _('نشطة حالياً')
    COMPLETED = 'CMP', _('منتهية')
    CANCELLED = 'CNL', _('ملغاة')

class CaseStatus(models.TextChoices):
    PENDING = 'PND', _('قيد الانتظار')
    REVIEWING = 'RVW', _('قيد المراجعة')
    APPROVED = 'APP', _('تمت الموافقة')
    REJECTED = 'REJ', _('مرفوض')
    DEFERRED = 'DEF', _('مؤجل لجلسة أخرى')

class ReferralStatus(models.TextChoices):
    ISSUED = 'ISS', _('تم الإصدار')
    ACCEPTED = 'ACC', _('مقبول في المركز')
    COMPLETED = 'CMP', _('تم تقديم الخدمة')
    CANCELLED = 'CNL', _('ملغي')

class DocumentTypeChoices(models.TextChoices):
    NATIONAL_ID = 'NID', _('بطاقة الرقم القومي')
    MEDICAL_REPORT = 'REP', _('تقرير طبي')
    LAB_RESULTS = 'LAB', _('نتائج التحاليل')
    RADIOLOGY = 'RAD', _('الأشعة')