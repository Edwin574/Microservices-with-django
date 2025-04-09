import os
from django.core.wsgi import get_wsgi_application

# Point to the settings of the accounts app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts.settings')

# Get the WSGI application callable
application = get_wsgi_application()
