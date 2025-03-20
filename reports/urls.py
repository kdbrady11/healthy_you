from django.urls import path
from . import views

# Define URL patterns for the 'reports' application
urlpatterns = [
    # Path for the report dashboard view
    path('dashboard/', views.report_dashboard, name='report_dashboard'),
]
