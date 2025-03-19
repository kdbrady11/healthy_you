from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.medications_dashboard, name='medications_dashboard'),
    path('create/', views.medication_create, name='medication_create'),
    path('edit/<int:med_id>/', views.medication_edit, name='medication_edit'),
    path('add-dose/<int:med_id>/', views.add_dose_time, name='add_dose_time'),
    path('update/<int:log_id>/', views.update_medication_log, name='update_medication_log'),
]

