from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.health_dashboard, name='health_dashboard'),
    path('edit/<str:entry_date>/', views.health_edit_entry, name='health_edit_entry'),
]
