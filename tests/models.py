from django.contrib.auth.models import AbstractUser
from django.db import models

from user_deletion.managers import UserManagerMixin


class UserManager(UserManagerMixin, models.Manager):
    pass


class User(AbstractUser):
    name = models.CharField(max_length=255)
    notified = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.name
