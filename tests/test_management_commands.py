from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from .factories import UserFactory
from .models import User


MONTH = 1


@patch('user_deletion.apps.UserDeletionConfig.MONTH_NOTIFICATION', new=MONTH)
class TestUserNotifyManagementCommand(TestCase):
    def test_no_users(self):
        call_command('notify_users')

        self.assertEqual(len(mail.outbox), 0)

    def test_inactive_users(self):
        month_ago = timezone.now() - relativedelta(months=MONTH)
        user = UserFactory.create(last_login=month_ago, notified=False)

        call_command('notify_users')

        self.assertEqual(len(mail.outbox), 1)
        user.refresh_from_db()
        self.assertTrue(user.notified)

    def test_notified_users(self):
        year_ago = timezone.now() - relativedelta(months=MONTH)
        UserFactory.create(last_login=year_ago, notified=True)

        call_command('notify_users')

        self.assertEqual(len(mail.outbox), 0)


@patch('user_deletion.apps.UserDeletionConfig.MONTH_DELETION', new=MONTH)
class TestDeleteUsersManagementCommand(TestCase):
    def test_no_users(self):
        call_command('delete_users')
        self.assertEqual(len(mail.outbox), 0)

    def test_inactive_users(self):
        year_ago = timezone.now() - relativedelta(months=MONTH)
        user = UserFactory.create(last_login=year_ago, notified=True)

        call_command('delete_users')

        self.assertEqual(len(mail.outbox), 1)
        with self.assertRaises(User.DoesNotExist):
            user.refresh_from_db()
