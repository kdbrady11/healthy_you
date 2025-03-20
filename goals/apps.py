from django.apps import AppConfig


class GoalsConfig(AppConfig):
    """
    Configuration class for the Goals application.
    Handles application-specific configurations such as name and default field types.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default primary key field type
    name = 'goals'  # Name of the application
