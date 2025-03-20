from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Configuration class for the 'reports' application.
    Contains metadata and default settings for the app.
    """
    # Specifies the default auto field to use for primary keys
    default_auto_field = 'django.db.models.BigAutoField'

    # Name of the application
    name = 'reports'
