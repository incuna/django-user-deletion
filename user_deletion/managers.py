from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.utils import timezone


class UserDeletionManagerMixin:
    def users_to_notify(self):
        """Finds all users who have been inactive and not yet notified."""
        user_deletion_config = apps.get_app_config('user_deletion')

        threshold = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_NOTIFICATION,
        )
        return self.filter(last_login__lte=threshold, notified=False)

    def users_to_delete(self):
        """Finds all users who have been inactive and were notified."""
        user_deletion_config = apps.get_app_config('user_deletion')

        threshold = timezone.now() - relativedelta(
            months=user_deletion_config.MONTH_DELETION,
        )
        return self.filter(last_login__lte=threshold, notified=True)
