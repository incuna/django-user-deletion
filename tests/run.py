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
    INSTALLED_APPS=('user_deletion',),
    MIDDLEWARE_CLASSES=(),
)


if django.VERSION >= (1, 7):
    django.setup()


class TestRunner(ColourRunnerMixin, DiscoverRunner):
    """Enable colorised output."""


test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['tests'])
if failures:
    sys.exit(1)
