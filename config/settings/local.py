from .base import *

ENV_MAPPING = {
    'False': False,
    'false': False,
    'True': True,
    'true': True,
}

DEBUG = ENV_MAPPING.get(os.environ.get('DEBUG'), True)

if os.environ.get('DATABASE') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', ''),
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', ''),
            'PORT': '3306'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

INSTALLED_APPS += ['django_extensions']
