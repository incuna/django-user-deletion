import os
import sys

import dj_database_url
import django
from colour_runner.django_runner import ColourRunnerMixin
from django.conf import settings
from django.test.runner import DiscoverRunner


BASEDIR = os.path.dirname(os.path.dirname(__file__))

settings.configure(
    DATABASES={
        'default': dj_database_url.config(
            default='sqlite://{}/user_deletion.db'.format(BASEDIR),
        ),
    },
    INSTALLED_APPS=(
        'tests',
        'user_deletion',

        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
    ),
    MIDDLEWARE_CLASSES=(),

    AUTH_USER_MODEL='tests.User',
    SITE_ID=1,
    DEFAULT_FROM_EMAIL='from@example.com',
)


django.setup()


class TestRunner(ColourRunnerMixin, DiscoverRunner):
    """Enable colorised output."""


test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['tests'])
if failures:
    sys.exit(1)
