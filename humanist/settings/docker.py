from .base import *  # noqa

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

EMAIL_HOST = 'mailhost'
