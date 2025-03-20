from django.urls import path
from . import views

# URL patterns for the appointments application
urlpatterns = [
    # Dashboard view: Displays the appointment dashboard
    path('dashboard/', views.appointment_dashboard, name='appointment_dashboard'),

    # Create view: Displays a form to create a new appointment
    path('create/', views.appointment_create, name='appointment_create'),

    # Delete view: Handles the deletion of a specific appointment by ID
    path('delete/<int:appointment_id>/', views.appointment_delete, name='appointment_delete'),

    # Detail view: Displays detailed information about a specific appointment by primary key (pk)
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
]
