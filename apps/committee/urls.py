from django.urls import path
from . import views
from .views import CommitteeSessionCreateView, CommitteeSessionListView, CommitteeSessionDetailView, PendingCasesListView

app_name = 'committee'

urlpatterns = [
    # Committee Sessions Dashboard & Operations
    path('sessions/', CommitteeSessionListView.as_view(), name='sessions_list'),
    path('session/create/', CommitteeSessionCreateView.as_view(), name='session_create'),
    path('session/<int:pk>/', CommitteeSessionDetailView.as_view(), name='session_detail'),
    path('session/<int:pk>/add-cases/', views.session_add_cases, name='session_add_cases'),
    #path('session/<int:pk>/attach-case/', views.attach_case_to_session, name='attach_case_to_session'),
    
    # Medical Consultation Pipeline
    path('cases/pending/', PendingCasesListView.as_view(), name='pending_cases'),
    path('case/<int:pk>/recommendation/', views.add_recommendation, name='recommendation_form'),
    
    # Printing Actions Routing Matrix (Consolidated)
    path('session/<int:session_pk>/case/<int:case_pk>/recommendation/', views.add_recommendation, name='add_recommendation'),
    path('recommendation/<int:rec_id>/print/', views.print_recommendation, name='print_recommendation')
]