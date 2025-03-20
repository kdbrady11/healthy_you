from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.appointment_dashboard, name='appointment_dashboard'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('delete/<int:appointment_id>/', views.appointment_delete, name='appointment_delete'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
]
