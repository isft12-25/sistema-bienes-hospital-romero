from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_testing.sqlite3',
    }
}

ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

HOSPITAL_NAME = "Gestión de Bienes Patrimoniales - Hospital Melchor Romero (Testing)"