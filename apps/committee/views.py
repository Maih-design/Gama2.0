from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from apps.core.constants import SessionStatus, CaseStatus, ReferralStatus
from .models import CommitteeSession, CommitteeCase, CommitteeRecommendation, Patient
from .forms import CommitteeSessionForm, CommitteeCaseForm, CommitteeRecommendationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class CommitteeSessionListView(LoginRequiredMixin, ListView):
    model = CommitteeSession
    template_name = 'committee/sessions_list.html'
    context_object_name = 'sessions'
    paginate_by = 20

    def get_queryset(self):
        return CommitteeSession.objects.select_related('doctor').order_by('-session_date')


class CommitteeSessionCreateView(LoginRequiredMixin, CreateView):
    model = CommitteeSession
    form_class = CommitteeSessionForm
    template_name = 'committee/create_session.html'

    def form_valid(self, form):
        form.instance.status = SessionStatus.SCHEDULED
        response = super().form_valid(form)
        messages.success(self.request, _("تم إنشاء الجلسة بنجاح كجلسة معلقة."))
        return response

    def get_success_url(self):
        return reverse('committee:session_add_cases', kwargs={'pk': self.object.pk})


class CommitteeSessionDetailView(LoginRequiredMixin, DetailView):
    model = CommitteeSession
    template_name = 'committee/session_details.html'
    context_object_name = 'session_obj'

    def get_queryset(self):
        return CommitteeSession.objects.select_related('doctor').prefetch_related(
            'cases__patient',
            'cases__recommendation__procedure'
        )


@login_required
def session_add_cases(request, pk):
    session_obj = get_object_or_404(CommitteeSession, pk=pk)
    
    if request.method == 'POST':
        patient_ids = request.POST.getlist('selected_patients')
        if not patient_ids:
            messages.error(request, _("يرجى اختيار مريض واحد على الأقل لإضافته للجلسة."))
            return redirect('committee:session_add_cases', pk=session_obj.pk)
            
        with transaction.atomic():
            for p_id in patient_ids:
                patient = get_object_or_404(Patient, pk=p_id)
                CommitteeCase.objects.get_or_create(
                    patient=patient,
                    committee_session=session_obj,
                    defaults={'status': CaseStatus.PENDING}
                )
        messages.success(request, _("تمت إضافة الحالات المحددة إلى الجلسة بنجاح."))
        return redirect('committee:session_detail', pk=session_obj.pk)

    # Optimization: Filter out patients already present in this specific session
    existing_patient_ids = session_obj.cases.values_list('patient_id', flat=True)
    available_patients = Patient.objects.exclude(id__in=existing_patient_ids).order_by('-created_at')[:50]
    
    return render(request, 'committee/add_cases_to_session.html', {
        'session_obj': session_obj,
        'available_patients': available_patients
    })


class PendingCasesListView(LoginRequiredMixin, ListView):
    model = CommitteeCase
    template_name = 'committee/pending_cases.html'
    context_object_name = 'cases'
    paginate_by = 25

    def get_queryset(self):
        return CommitteeCase.objects.filter(
            status__in=[CaseStatus.PENDING, CaseStatus.REVIEWING]
        ).select_related('patient', 'committee_session__doctor').order_by('created_at')


@login_required
def add_recommendation(request, case_id):
    case = get_object_or_404(
        CommitteeCase.objects.select_related('patient', 'committee_session'), 
        pk=case_id
    )
    
    # Logic Hook: Try grabbing an existing recommendation for an update form loop
    recommendation = getattr(case, 'recommendation', None)

    if request.method == 'POST':
        form = CommitteeRecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            with transaction.atomic():
                rec = form.save(commit=False)
                rec.committee_case = case
                rec.save()
                
                # Check case management workflow updates
                case.status = CaseStatus.APPROVED
                case.save()
                
                # Helper calculation to close session dynamically if fully decided
                _evaluate_and_close_session(case.committee_session)

            messages.success(request, _("تم حفظ التوصية والقرار الطبي بنجاح."))
            
            if rec.procedure.requires_referral:
                return redirect('referrals:create_referral', case_id=case.id)
            else:
                return redirect('committee:print_recommendation', rec_id=rec.id)
    else:
        form = CommitteeRecommendationForm(instance=recommendation)

    return render(request, 'committee/recommendation_form.html', {
        'form': form,
        'case': case
    })


@login_required
def print_recommendation(request, rec_id):
    recommendation = get_object_or_404(
        CommitteeRecommendation.objects.select_related('committee_case__patient', 'procedure', 'committee_case__committee_session__doctor'),
        pk=rec_id
    )
    return render(request, 'print/recommendation_print.html', {'recommendation': recommendation})


@login_required
def _evaluate_and_close_session(session_obj):
    """
    Internal business engine workflow automation validation rules.
    Closes session automatically when all structural cases contain assigned recommendations.
    """
    total_cases = session_obj.cases.count()
    resolved_cases = session_obj.cases.filter(status__in=[CaseStatus.APPROVED, CaseStatus.REJECTED]).count()
    
    if total_cases > 0 and total_cases == resolved_cases:
        session_obj.status = SessionStatus.COMPLETED
        session_obj.save()
