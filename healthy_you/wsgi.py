"""
WSGI config for the Healthy You project.

This file contains the configuration for running the project using the WSGI (Web Server Gateway Interface).
WSGI acts as an interface between web servers and your Django application.

For more details, refer to:
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthy_you.settings')

# Get the WSGI application callable
application = get_wsgi_application()
