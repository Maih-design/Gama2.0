from django.urls import path
from .views import IssuedReferralsListView, PendingReferralsListView
from . import views
app_name = 'referrals'

urlpatterns = [
    # Referrals Verification Queues
    path('pending/', PendingReferralsListView.as_view(), name='pending_referrals'),
    path('issued/', IssuedReferralsListView.as_view(), name='issued_referrals'),
    
    # Referral Issuance Infrastructure Forms
    path('case/<int:case_pk>/create/', views.create_referral, name='create_referral_from_case'),
    path('case/<int:case_pk>/assign/', views.create_referral, name='assign_center_and_create'),
    
    # Active Referral Operations Lifecycle Controls
    #path('<int:pk>/update-center/', views.update_referral_center, name='update_referral_center'),
    path('<int:pk>/cancel/', views.cancel_referral, name='cancel_referral'),
    path('<int:pk>/reissue/', views.reissue_referral, name='reissue_referral'),
    
    # Printing Actions Routing Matrix (Consolidated)
    path('<int:pk>/print/', views.print_referral, name='print_referral'),
]