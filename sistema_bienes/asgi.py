import os
from django.core.asgi import get_asgi_application
from decouple import config

environment = config('DJANGO_ENV', default='development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'sistema_bienes.settings.{environment}')

application = get_asgi_application()