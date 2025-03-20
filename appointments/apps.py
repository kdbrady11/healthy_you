from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """
    Configuration class for the appointments application.
    Defines the application name and default auto field setting.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField for auto-generated primary keys
    name = 'appointments'  # The name of the app, matching the directory name
