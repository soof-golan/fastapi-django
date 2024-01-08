from typing import Self, ClassVar

from django.db import models

from fastapi_django.db.base import DbBaseModel, DefaultQuerySet
from django.db import models

from fastapi_django.db.base import DbBaseModel


class UserManager(models.Manager["User"]):
    def get_queryset(self: Self) -> DefaultQuerySet["User"]:
        return DefaultQuerySet(self.model, using=self._db).exclude(
            deleted_at__isnull=False,
        )


class User(DbBaseModel):
    objects: ClassVar[UserManager] = UserManager()

    firebase_id = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )
