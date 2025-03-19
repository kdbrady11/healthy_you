from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_metric, name='add_metric'),
    path('view/', views.view_metrics, name='view_metrics'),
]