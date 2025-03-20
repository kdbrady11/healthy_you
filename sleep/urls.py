from django.urls import path
from . import views

# Define URL patterns for the sleep application
urlpatterns = [
    # Route for the sleep dashboard
    path('dashboard/', views.sleep_dashboard, name='sleep_dashboard'),
]
