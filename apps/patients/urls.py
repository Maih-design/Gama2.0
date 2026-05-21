from django.urls import path
from . import views
from .views import PatientCreateView, PatientProfileView, PatientListView, PatientUpdateView

app_name = 'patients'

urlpatterns = [
    # Patient Profile & SRE Registries Data Pipelines
    path('create/', PatientCreateView.as_view(), name='patient_create'),
    path('profile/<int:pk>/', PatientProfileView.as_view(), name='patient_profile'),
    path('patient/list', PatientListView.as_view(), name='patient_list'),
    # Printing Actions Routing Matrix (Consolidated Checklist Document)
    path('patient/<int:patient_pk>/print-checklist/', views.documents_checklist_print, name='documents_checklist_print'),
    path('patient/update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('patient/upload/<int:pk>/', views.upload_patient_document, name='upload_document'),
]