from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.goal_dashboard, name='goal_dashboard'),
    path('create/', views.goal_create, name='goal_create'),
    path('edit/<int:goal_id>/', views.goal_edit, name='goal_edit'),
]
