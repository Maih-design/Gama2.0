from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Patient, PatientDocument
from .forms import PatientForm, PatientDocumentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 25

    def get_queryset(self):
        return Patient.objects.all().order_by('-created_at')


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def get_success_url(self):
        messages.success(self.request, _("تم تسجيل المريض بنجاح."))
        return reverse('patients:patient_profile', kwargs={'pk': self.object.pk})


class PatientProfileView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_profile.html'
    context_object_name = 'patient'

    def get_queryset(self):
        return Patient.objects.prefetch_related('documents', 'committee_cases__committee_session')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_form'] = PatientDocumentForm()
        return context


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def get_success_url(self):
        messages.success(self.request, _("تم تحديث بيانات المريض بنجاح."))
        return reverse('patients:patient_profile', kwargs={'pk': self.object.pk})


@login_required
def upload_patient_document(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientDocumentForm(request.POST, request.FILES)
        if form.is_validate():
            document = form.save(commit=False)
            document.patient = patient
            document.save()
            messages.success(request, _("تم رفع المستند بنجاح."))
        else:
            messages.error(request, _("فشل في رفع المستند. يرجى التحقق من الحقول."))
    return redirect('patients:patient_profile', pk=patient.pk)

@login_required
def documents_checklist_print(request, patient_pk):
    """
    Premium print template view generating the official checklist of required 
    documents and credentials needed for medical committee review.
    """
    patient = get_object_or_404(Patient, pk=patient_pk)
    context = {
        'patient': patient,
    }
    return render(request, 'print/documents_checklist_print.html', context)