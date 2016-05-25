from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils import translation

User = get_user_model()
user_deletion_config = apps.get_app_config('user_deletion')


class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        users = User.objects.users_to_delete()
        site = Site.objects.get_current()
        user_deletion_config.deletion_notification_class(
            user=None,
            site=site,
            users=users,
        ).notify()
        users.delete()
