from django.apps import AppConfig


class SleepConfig(AppConfig):
    """
    Configuration class for the 'sleep' application.
    Specifies application metadata and default settings.
    """
    # Default primary key field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Application name
    name = 'sleep'
