from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase

from user_deletion.notifications import (
    AccountDeletedNotification,
    AccountInactiveNotification,
)
from .factories import UserFactory


class TestAccountDeletedNotification(TestCase):
    def test_notification(self):
        user = UserFactory.create()
        site = Site.objects.get_current()

        AccountDeletedNotification(user=None, site=site, users=[user]).notify()

        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Your account has been deleted')
        self.assertIn('You were informed', email.body)


class TestAccountInactiveNotification(TestCase):
    def test_notification(self):
        user = UserFactory.create()
        site = Site.objects.get_current()

        AccountInactiveNotification(user=None, site=site, users=[user]).notify()

        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Re-activate your account')
        self.assertIn('We have noticed', email.body)
        self.assertIn('example.com', email.body)
