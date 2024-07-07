import os

from general import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = []#server to deploy to/ domain its going to be running on


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['NAME'],
        'USER': os.environ['USER'],
        'PASSWORD': os.environ['PASSWORD'],
        'HOST': os.environ['HOST'],
        'PORT': os.environ['PORT'],
    }
}
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= os.environ['EMAIL_HOST'],
EMAIL_HOST_USER=os.environ['EMAIL_HOST_USER'],
EMAIL_HOST_PASSWORD=os.environ['EMAIL_HOST_PASSWORD'],
EMAIL_PORT=os.environ['EMAIL_PORT']
DEFAULT_FROM_EMAIL='info@jagudabank.com'