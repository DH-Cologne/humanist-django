from .base import *  # noqa
from os import environ

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = INTERNAL_IPS + ['']

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'NAME': 'humanist',
        'USER': 'humanist',
        'PASSWORD': 'humanist',
        'HOST': 'db'
    },
}

CACHES['default']['LOCATION'] = 'redis://cache:6379/humanist'

HAYSTACK_CONNECTIONS['default']['URL'] = 'http://search:9200/'

EMAIL_HOST = 'mailhost'

if not 'BASE_URL' in environ:
  raise Exception("BASE_URL not set for docker setup")

BASE_URL = environ.get('BASE_URL', 'https://miskatonic.hki.uni-koeln.de')
