from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.utils import timezone


user_deletion_config = apps.get_app_config('user_deletion')


class UserManagerMixin:
    def users_to_notify(self):
        """Finds all users who have been inactive and not yet notified."""
        last_login = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_NOTIFICATION,
        )
        return self.filter(last_login__lte=last_login, notified=False)

    def users_to_delete(self):
        """Finds all users who have been inactive and were notified."""
        one_year = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_DELETION,
        )
        return self.filter(last_login__lte=one_year, notified=True)
