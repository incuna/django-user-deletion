from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils import translation

from ...notifications import AccountDeletedNotification

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        users = User.objects.users_to_delete()
        site = Site.objects.get_current()
        AccountDeletedNotification(user=None, site=site, users=users).notify()
        users.delete()
