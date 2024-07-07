import os

from .general import *

SECRET_KEY = 'django-insecure-y(40*&#p%ir&na6(s0+*nnyyg17gq5*i!j9)s8#^uo-o@r#@2n'

DEBUG = True
ALLOWED_HOSTS = []#server to deploy to/ domain its going to be running on

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account_db',
        'USER': 'root',
        'PASSWORD': '#Ozunmba1oflagos',
        'HOST': 'localhost',
    }
}

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'localhost',
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=2525
DEFAULT_FROM_EMAIL='info@jagudabank.com'