from django.contrib import admin
from django.urls import path, include

# URL patterns for the core Healthy You project
urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Modular app URLs
    path('accounts/', include('accounts.urls')),  # User authentication and management
    path('health/', include('health.urls')),  # Health tracking functionality
    path('medications/', include('medications.urls')),  # Medication tracking and management
    path('sleep/', include('sleep.urls')),  # Sleep tracking functionality
    path('goals/', include('goals.urls')),  # Goal-setting and tracking
    path('appointments/', include('appointments.urls')),  # Appointment scheduling and management
    path('reports/', include('reports.urls')),  # Reports and analytics
]
