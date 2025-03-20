from django.urls import path
from . import views

# Define URL patterns for the medications app
urlpatterns = [
    path('dashboard/', views.medications_dashboard, name='medications_dashboard'),
    # Dashboard view to display all medications and related details

    path('create/', views.medication_create, name='medication_create'),
    # View for creating a new medication

    path('edit/<int:med_id>/', views.medication_edit, name='medication_edit'),
    # View for editing an existing medication, identified by its ID

    path('add-dose/<int:med_id>/', views.add_dose_time, name='add_dose_time'),
    # View for adding a dose time to a medication, identified by its ID

    path('update/<int:log_id>/', views.update_medication_log, name='update_medication_log'),
    # View for updating a medication log, identified by its log ID
]

