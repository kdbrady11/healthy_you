"""
ASGI config for the Healthy You project.

This file exposes the ASGI callable as a module-level variable named `application`.
ASGI (Asynchronous Server Gateway Interface) is used for serving your project
asynchronously and is necessary for supporting asynchronous frameworks and features.

For more information, see:
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthy_you.settings')

# Get the ASGI application callable
application = get_asgi_application()
