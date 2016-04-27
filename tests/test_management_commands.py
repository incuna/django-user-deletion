from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from .factories import UserFactory


MONTH = 1


class TestUserNotifyManagementCommand(TestCase):
    def test_no_users(self):
        call_command('notify_users')
        self.assertFalse(len(mail.outbox))

    def test_inactive_users(self):
        month_ago = timezone.now() - relativedelta(months=13)
        UserFactory.create(last_login=month_ago)

        call_command('notify_users')

        self.assertEqual(len(mail.outbox), 1)

    @patch('user_deletion.apps.UserDeletionConfig.MONTH_NOTIFICATION', new=MONTH)
    def test_inactive_users_config(self):
        month_ago = timezone.now() - relativedelta(months=MONTH + 1)
        UserFactory.create(last_login=month_ago)

        call_command('notify_users')

        self.assertEqual(len(mail.outbox), 1)

    def test_email(self):
        year_ago = timezone.now() - relativedelta(months=12)
        UserFactory.create(last_login=year_ago)
        call_command('notify_users')

        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Re-activate your account')
        self.assertIn('We have noticed', email.body)

    def test_notified_users(self):
        year_ago = timezone.now() - relativedelta(months=13)
        UserFactory.create(last_login=year_ago, notified=True)

        call_command('notify_users')
        self.assertFalse(len(mail.outbox))


class TestDeleteUsersManagementCommand(TestCase):
    def test_no_users(self):
        call_command('delete_users')
        self.assertFalse(len(mail.outbox))

    def test_inactive_users(self):
        year_ago = timezone.now() - relativedelta(months=13)
        UserFactory.create(last_login=year_ago, notified=True)

        call_command('delete_users')

        self.assertEqual(len(mail.outbox), 1)

    @patch('user_deletion.apps.UserDeletionConfig.MONTH_DELETION', new=MONTH)
    def test_inactive_users_config(self):
        month_ago = timezone.now() - relativedelta(months=MONTH + 1)
        UserFactory.create(last_login=month_ago, notified=True)

        call_command('delete_users')

        self.assertEqual(len(mail.outbox), 1)

    def test_email(self):
        year_ago = timezone.now() - relativedelta(months=13)
        UserFactory.create(last_login=year_ago, notified=True)
        call_command('delete_users')

        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Your account has been deleted')
        self.assertIn('You were informed', email.body)
