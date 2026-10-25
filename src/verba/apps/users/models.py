from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    username: models.CharField = models.CharField(
        unique=True, blank=False, null=False, max_length=100
    )
    hashed_password: models.CharField = models.CharField(
        unique=True, blank=False, null=False
    )
    created_at: models.DateField = models.DateField(
        auto_now=True,
    )
    updated_at: models.DateField = models.DateField(
        null=True,
        blank=True,
        default=None,
    )
