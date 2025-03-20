from django.apps import AppConfig


class HealthConfig(AppConfig):
    """
    Application configuration for the 'health' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default auto field type for primary keys.
    name = 'health'  # Name of the application as specified in the project structure.
