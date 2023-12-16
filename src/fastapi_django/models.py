import datetime
import uuid
from typing import ClassVar, Self

from asgiref.sync import sync_to_async
from django.db import models


class DefaultQuerySet(models.QuerySet):
    def delete(self: Self) -> Self:
        return self.update(deleted_at=datetime.datetime.now(tz=datetime.UTC))

    def hard_delete(self: Self) -> Self:
        return super().delete()

    ahard_delete = sync_to_async(hard_delete)
    ahard_delete.alters_data = True
    ahard_delete.queryset_only = True

    def restore(self):
        # Undo soft delete
        return super().update(deleted_at=None)

    arestore = sync_to_async(restore)
    arestore.alters_data = True
    arestore.queryset_only = True


class DefaultManager(models.Manager):
    def get_queryset(self):
        return DefaultQuerySet(self.model, using=self._db).exclude(
            deleted_at__isnull=True
        )


class DbBaseModel(models.Model):
    objects = DefaultManager()

    class Meta:
        abstract = True
        indexes: ClassVar[list[models.Index]] = [
            # Home for composite indexes
            models.Index(
                fields=["id", "deleted_at"], name="%(class)s_id_deleted_at_idx"
            ),
        ]
        constraints: ClassVar[list[models.UniqueConstraint]] = [
            # Home for unique constraints
        ]

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        db_default="uuid_generate_v1mc()",
        default=uuid.uuid1,
        unique=True,
    )


class User(DbBaseModel):
    firebase_id = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )
