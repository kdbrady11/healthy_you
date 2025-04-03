from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


# URL patterns for the accounts app
urlpatterns = [
    path("", views.homepage, name="home"),  # Homepage view at the root of the accounts app

    # Registration Page
    path('register/', views.register, name='register'),  # Route for user registration

    # Login Page
    path('login/', views.user_login, name='login'),  # Route for user login

    # Logout Endpoint
    path('logout/', views.user_logout, name='logout'),  # Route for logging out users

    # User Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),  # Route for user dashboard
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
