from django.db import models

from verba.apps.users.models import Users


class Notes(models.Model):
    first_note: models.TextField = models.TextField(
        unique=True,
    )
    secound_note: models.TextField = models.TextField(
        unique=True, blank=True, null=True
    )
    user: models.ForeignKey = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    created_at: models.DateField = models.DateField(
        auto_now=True,
    )
    updated_at: models.DateField = models.DateField(
        null=True,
        blank=True,
        default=None,
    )
