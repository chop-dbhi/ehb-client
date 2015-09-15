#from distutils.core import setup
#
from setuptools import setup
#
kwargs = {
   
    # Dependencies
    'install_requires': [
    ],

    'test_suite': 'test_suite',

    # Test dependencies
    'tests_require': [
        'django-guardian',
        'django-haystack',
        'whoosh',
        'coverage',
    ],

    # Optional dependencies
    'extras_require': {
        # Granular permission
        'permissions': ['django-guardian'],
        # Search
        'search': ['django-haystack'],
    },

   
}




setup(**kwargs)
