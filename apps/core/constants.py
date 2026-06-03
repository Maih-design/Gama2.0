from django.db import models
from django.utils.translation import gettext_lazy as _

class GenderChoices(models.TextChoices):
    MALE = 'M', _('ذكر')
    FEMALE = 'F', _('أنثى')

class GovernorateChoices(models.TextChoices):
    ASSIUT = 'AST', _('اسيوط')
    BEHEIRA = 'BHR', _('البحيرة')
    GIZA = 'GIZ', _('الجيزة')
    DAKAHLIA = 'DKH', _('الدقهلية')
    SHARQIA = 'SHR', _('الشرقية')
    GHARBIA = 'GHB', _('الغربية')
    FAYOUM = 'FYM', _('الفيوم')
    CAIRO = 'CAI', _('القاهرة')
    QALYUBIA = 'QLY', _('القليوبية')
    MENOFIA = 'MNF', _('المنوفية')
    MINYA = 'MNY', _('المنيا')
    BENI_SUEF = 'BNS', _('بنى سويف')
    DAMIETTA = 'DMT', _('دمياط')
    SOHAG = 'SHG', _('سوهاج')
    NORTH_SINAI = 'NSN', _('شمال سيناء')
    NW_DELTA = 'NWD', _('شمال غرب الدلتا')
    QENA = 'QNA', _('قنا')
    KAFR_EL_SHEIKH = 'KSH', _('كفر الشيخ')
    RED_SEA = 'RDS', _('البحر الاحمر')
    NEW_VALLEY = 'NWV', _('الوادى الجديد')
    MATROUH = 'MTR', _('مطروح')
    # Expandable as required by the business region

class BranchChoices(models.TextChoices):
    ASSIUT = 'AST', _('فرع اسيوط')
    BEHEIRA = 'BHR', _('فرع البحيرة')
    GIZA = 'GIZ', _('فرع الجيزة')
    DAKAHLIA = 'DKH', _('فرع الدقهلية')
    SHARQIA = 'SHR', _('فرع الشرقية')
    GHARBIA = 'GHB', _('فرع الغربية')
    FAYOUM = 'FYM', _('فرع الفيوم')
    CAIRO = 'CAI', _('فرع القاهرة')
    QALYUBIA = 'QLY', _('فرع القليوبية')
    MENOFIA = 'MNF', _('فرع المنوفية')
    MINYA = 'MNY', _('فرع المنيا')
    BENI_SUEF = 'BNS', _('فرع بنى سويف')
    DAMIETTA = 'DMT', _('فرع دمياط')
    SOHAG = 'SHG', _('فرع سوهاج')
    NORTH_SINAI = 'NSN', _('فرع شمال سيناء')
    NW_DELTA = 'NWD', _('فرع شمال غرب الدلتا')
    QENA = 'QNA', _('فرع قنا')
    KAFR_EL_SHEIKH = 'KSH', _('فرع كفر الشيخ')
    RED_SEA = 'RDS', _('منطقة البحر الاحمر')
    NEW_VALLEY = 'NWV', _('منطقة الوادى الجديد')
    MATROUH = 'MTR', _('منطقة مطروح')


class SessionStatus(models.TextChoices):
    ACTIVE = 'ACT', _('نشطة حالياً')
    CLOSED = 'CMP', _('منتهية')

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

class InsuranceLawChoices(models.TextChoices):
    RETAIRED = 'RET', _('معاش ق79')
    STUDENT = 'STD', _('طلبة')
    CHILD = 'CID', _('مواليد ق99')
    EMPLOYE = 'EMP', _('موظف ق79')