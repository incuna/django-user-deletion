from django.apps import AppConfig

from .notifications import AccountDeletedNotification, AccountInactiveNotification


class UserDeletionConfig(AppConfig):
    name = 'user_deletion'

    # users are notificed after 12 months of inactivity
    MONTH_NOTIFICATION = 12
    # users are deleted after 13 months
    MONTH_DELETION = 13

    deletion_notification_class = AccountDeletedNotification
    inactive_notification_class = AccountInactiveNotification
