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
from django.db.models import Q


class CommitteeSessionListView(LoginRequiredMixin, ListView):

    model = CommitteeSession
    template_name = 'committee/sessions_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return CommitteeSession.objects.select_related(
            'doctor'
        ).order_by('-session_date')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # الجلسة المفتوحة الحالية
        preparing_session = CommitteeSession.objects.filter(
            status=SessionStatus.PREPARING
        ).first()

        context['preparing_session'] = preparing_session

        # باقي الجلسات
        previous_sessions = CommitteeSession.objects.all()

        if preparing_session:
            previous_sessions = previous_sessions.exclude(id=preparing_session.id)

        context['previous_sessions'] = previous_sessions.order_by('-session_date')

        return context


class CommitteeSessionCreateView(LoginRequiredMixin, CreateView):
    model = CommitteeSession
    form_class = CommitteeSessionForm
    template_name = 'committee/create_session.html'

    @transaction.atomic
    def form_valid(self, form):

        CommitteeSession.objects.filter(
            status=CommitteeSession.status.PREPARING
        ).update(
            status=CommitteeSession.status.COMPLETED
        )



        form.instance.status = CommitteeSession.status.PREPARING

        response = super().form_valid(form)

        messages.success(
            self.request,
            _("تم إنشاء قيد التحضير وتحويل الجلسة السابقة الى مكتملة.")
        )

        return response

    def get_success_url(self):
        return reverse(
            'committee:session_add_cases',
            kwargs={'pk': self.object.pk}
        )



class CommitteeSessionDetailView(LoginRequiredMixin, DetailView):
    model = CommitteeSession
    template_name = "committee/session_details.html"
    context_object_name = "session"

    def get_queryset(self):
        return (
            CommitteeSession.objects
            .select_related("doctor")
            .prefetch_related(
                "cases__patient",
                "cases__recommendation__procedure",
                "cases__referrals__referral_center",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        show_print_modal = self.request.GET.get("show_print_modal") == "1"

        missing_cases = self.object.cases.filter(
            recommendation__isnull=True
        )

        context["show_print_modal"] = show_print_modal
        context["missing_cases"] = missing_cases
        context["missing_cases_count"] = missing_cases.count()

        return context


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
def add_recommendation(request, session_pk, case_pk):
    case = get_object_or_404(
    CommitteeCase.objects.select_related('patient', 'committee_session'),
    pk=case_pk,
    committee_session_id=session_pk
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
                
            messages.success(request, _("تم حفظ التوصية والقرار الطبي بنجاح."))
            
            if rec.procedure.requires_referral:
                return redirect('referrals:create_referral', case_pk=case.id)
            else:
                return redirect('committee:print_recommendation', rec_id=rec.id)
    else:
        form = CommitteeRecommendationForm(instance=recommendation)

    return render(request, 'committee/recommendation_form.html', {
        'form': form,
        'case': case
    })


@login_required
def print_session(request, pk):

    session = get_object_or_404(
        CommitteeSession.objects.select_related("doctor"),
        pk=pk
    )

    # لا يسمح بطباعة جلسة قيد التجهيز
    if session.status == SessionStatus.PREPARING:
        messages.error(
            request,
            "لا يمكن طباعة جلسة قيد التجهيز، يجب إنهاء الجلسة أولاً."
        )
        return redirect(
            "committee:session_detail",
            pk=session.pk
        )

    force_print = request.GET.get("force") == "1"

    missing_cases = session.cases.filter(
        recommendation__isnull=True
    )

    if missing_cases.exists() and not force_print:
        return redirect(
            f"{reverse('committee:session_detail', kwargs={'pk': session.pk})}?show_print_modal=1"
        )

    return render(
        request,
        "print/session_print.html",
        {
            "session": session,
        }
    )