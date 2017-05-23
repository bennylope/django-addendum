"""
Configuration file for py.test
"""

import django


def pytest_configure():
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        USE_I18N=True,
        ROOT_URLCONF="tests.urls",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "test.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "addendum",
        ],
        # TODO conditionally include south
        MIDDLEWARE_CLASSES=(),  # Silence Django 1.7 warnings
        SITE_ID=1,
        FIXTURE_DIRS=['tests/fixtures'],
        LANGUAGE_CODE='es',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.i18n',
                    ]
                }
            },
        ],
    )
    try:
        django.setup()
    except AttributeError:
        pass
