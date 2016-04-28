from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.test import TestCase
from django.utils import timezone

from .factories import UserFactory
from .models import User


user_deletion_config = apps.get_app_config('user_deletion')


class TestUserDeletionManager(TestCase):
    def test_users_to_notify(self):
        last_login = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_NOTIFICATION,
        )
        user = UserFactory.create(last_login=last_login, notified=False)
        users = User.objects.users_to_notify()

        self.assertCountEqual(users, [user])

    def test_users_not_to_notify(self):
        user = UserFactory.create(last_login=timezone.now(), notified=False)
        users = User.objects.users_to_notify()

        self.assertNotIn(user, users)

    def test_users_already_notified(self):
        last_login = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_NOTIFICATION,
        )
        user = UserFactory.create(last_login=last_login, notified=True)
        users = User.objects.users_to_notify()

        self.assertNotIn(user, users)

    def test_users_to_delete(self):
        last_login = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_DELETION,
        )
        user = UserFactory.create(last_login=last_login, notified=True)
        users = User.objects.users_to_delete()

        self.assertCountEqual(users, [user])

    def test_users_not_to_delete(self):
        user = UserFactory.create(last_login=timezone.now(), notified=False)
        users = User.objects.users_to_delete()

        self.assertNotIn(user, users)

    def test_users_to_delete_not_notified(self):
        last_login = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_DELETION,
        )
        user = UserFactory.create(last_login=last_login, notified=False)
        users = User.objects.users_to_delete()

        self.assertNotIn(user, users)
