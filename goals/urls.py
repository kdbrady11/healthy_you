from django.urls import path
from . import views

# Define URL patterns for the Goals application
urlpatterns = [
    # Dashboard view: Displays the list of goals
    path('dashboard/', views.goal_dashboard, name='goal_dashboard'),

    # Create view: Allows users to create a new goal
    path('create/', views.goal_create, name='goal_create'),

    # Edit view: Allows users to edit an existing goal (based on goal_id)
    path('edit/<int:goal_id>/', views.goal_edit, name='goal_edit'),
]
