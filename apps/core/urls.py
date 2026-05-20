from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Operational Dashboard & Gateway Views
    path('', views.homepage, name='homepage'),
    path('api/patients/search/', views.patient_search_api, name='patient_search_api'),
]