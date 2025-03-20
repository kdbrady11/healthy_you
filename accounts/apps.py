from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the 'accounts' application.
    Sets the default auto field for model primary keys
    and defines the application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default field for primary keys
    name = 'accounts'  # Name of the application

