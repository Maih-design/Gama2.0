from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Dynamic imports based on your app architecture setup
# Adjust the app names/paths if your models live elsewhere
from apps.patients.models import Patient
from apps.committee.models import CommitteeSession, CommitteeCase
from apps.referrals.models import Referral

#@login_required
def homepage(request):
    """
    Main premium operational control dashboard gateway.
    Aggregates high-level healthcare operations metrics for the landing interface.
    """
    # Fetch real-time operation metrics for the SaaS dashboard view
    active_session = CommitteeSession.objects.filter(is_active=True).first()
    pending_cases_count = CommitteeCase.objects.filter(status='PEN').count()
    active_referrals_count = Referral.objects.filter(status="ISSUED").count()
    
    context = {
        'active_session': active_session,
        'pending_cases_count': pending_cases_count,
        'active_referrals_count': active_referrals_count,
    }
    return render(request, 'core/homepage.html', context)


def patient_search_api(request):
    """
    High-performance AJAX endpoint for real-time patient search pipeline 
    integrated inside the committee session attachment workspace matrix.
    """
    query = request.GET.get('q', '').strip()
    
    # Enforce a minimum safe query boundary limit before evaluating database hits
    if len(query) < 3:
        return JsonResponse([], safe=False)
        
    try:
        # Evaluate both fields gracefully using a single query execution branch
        matched_patients = Patient.objects.filter(
            Q(full_name__icontains=query) | 
            Q(national_id__icontains=query)
        )[:10]  # Hard limit performance boundary envelope
        
        # Format dataset JSON structure expected by static/js/referrals.js pipeline
        data = [
            {
                'id': patient.pk,
                'full_name': patient.full_name,
                'national_id': patient.national_id,
                'diagnosis': patient.diagnosis,
            }
            for patient in matched_patients
        ]
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        # Fallback safe error handling boundary matrix
        return JsonResponse({'error': str(e)}, status=500)