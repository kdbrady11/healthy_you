from django.urls import path
from . import views

# Application URL configuration for the 'health' app
urlpatterns = [
    # URL for the health dashboard
    path(
        'dashboard/',
        views.health_dashboard,
        name='health_dashboard',  # Named route for reverse URL resolution
    ),

    # URL for editing a specific health entry by its date
    path(
        'edit/<str:entry_date>/',
        views.health_edit_entry,
        name='health_edit_entry',  # Named route for reverse URL resolution
    ),
]
