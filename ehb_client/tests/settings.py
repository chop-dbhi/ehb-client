import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'tests.db'),
    }
}

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tests',
    'tests.cases.request',
)

SITE_ID = 1

EHB_LOG=0

ANONYMOUS_USER_ID = -1

TEST_RUNNER = 'tests.runner.ProfilingTestRunner'
TEST_PROFILE = 'unittest.profile'

SECRET_KEY = 'dfa'

LOGGING = {
    'version': 1,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'avocado': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
