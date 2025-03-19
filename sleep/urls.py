from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.sleep_dashboard, name='sleep_dashboard'),
]
