from django.apps import AppConfig


class UserDeletionConfig(AppConfig):
    name = 'user_deletion'

    # users are notificed after 12 months of inactivity
    MONTH_NOTIFICATION = 12
    # users are deleted after 13 months
    MONTH_DELETION = 13
