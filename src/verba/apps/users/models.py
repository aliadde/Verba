from typing import ClassVar

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        if not password:
            raise ValueError("The password must be set")

        if extra_fields.get("email"):
            extra_fields["email"] = self.normalize_email(extra_fields["email"])

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        # sync your custom field with the hashed password
        user.hashed_password = user.password
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class Users(AbstractUser):
    username: models.CharField = models.CharField(
        unique=True, blank=False, null=False, max_length=100
    )
    hashed_password: models.CharField = models.CharField(
        unique=True, blank=False, null=False, max_length=128
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects: ClassVar[UserManager] = UserManager()  # type: ignore[assignment]
