from datetime import datetime
from io import StringIO

from dateutil.relativedelta import relativedelta
from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from .factories import UserFactory


class TestUserNotifyManagementCommand(TestCase):
    def setUp(self):
        self.stdout = StringIO()

    def test_no_users(self):
        call_command('notify_users')
        self.assertFalse(len(mail.outbox))

    def test_inactive_users(self):
        year_ago = datetime.now() + relativedelta(months=-12)
        UserFactory.create(last_login=year_ago)

        call_command('notify_users')

        self.assertEqual(len(mail.outbox), 1)

    def test_email(self):
        year_ago = datetime.now() + relativedelta(months=-12)
        UserFactory.create(last_login=year_ago)
        call_command('notify_users')

        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Re-activate your account')
        self.assertIn('We have noticed', email.body)

    def test_active_users(self):
        # user was notified before
        year_ago = datetime.now() + relativedelta(months=-13)
        UserFactory.create(last_login=year_ago, notified=True)

        call_command('notify_users')
        self.assertFalse(len(mail.outbox))
