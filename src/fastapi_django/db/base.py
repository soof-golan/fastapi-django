"""Hide the complexity of soft deletes and uuids from the rest of the app."""

import datetime
import uuid
from typing import Self, TypeVar

from asgiref.sync import sync_to_async
from django.db import models
from django.db.models.query import QuerySet, Q
from django_stubs_ext.db.models import TypedModelMeta

from fastapi_django.db.primary_key import uuid_generate_v1mc


class DefaultQuerySet(models.QuerySet):
    def delete(self: Self) -> tuple[int, dict[str, int]]:
        self.update(deleted_at=datetime.datetime.now(tz=datetime.UTC))
        return 0, {}

    def hard_delete(self: Self) -> tuple[int, dict[str, int]]:
        return super().delete()

    ahard_delete = sync_to_async(hard_delete)
    ahard_delete.alters_data = True  # type: ignore[attr-defined]
    ahard_delete.queryset_only = True  # type: ignore[attr-defined]

    def restore(self) -> int:
        # Undo soft delete
        return self.update(deleted_at=None)

    arestore = sync_to_async(restore)
    arestore.alters_data = True  # type: ignore[attr-defined]
    arestore.queryset_only = True  # type: ignore[attr-defined]


class DefaultManager(models.Manager.from_queryset(DefaultQuerySet)):
    def get_queryset(self: Self):
        return super().get_queryset().exclude(deleted_at__isnull=False)


class DbBaseModel(models.Model):
    """All App models should inherit from this class.

    This class provides the following features:
     - uuid v1 with random MAC address as primary key (A compromise between
         sequential and random ids)
     - updated_at and created_at timestamps
     - soft deletes
    """

    objects = DefaultManager()

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid_generate_v1mc,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta(TypedModelMeta):
        abstract = True
        indexes = [
            # Home for composite indexes
            models.Index(
                fields=["id", "deleted_at"], name="%(class)s_id_deleted_at_idx"
            ),
        ]
        constraints = [
            # Home for unique constraints
        ]
