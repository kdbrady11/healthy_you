from django.apps import AppConfig


class MedicationsConfig(AppConfig):
    """
    Configuration class for the Medications app.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default primary key type for models
    name = 'medications'  # Name of the app as registered in Django settings
    verbose_name = 'Medications Management'  # Human-readable name for the app
