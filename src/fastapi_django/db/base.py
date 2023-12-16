"""Hide the complexity of soft deletes and uuids from the rest of the app."""

import datetime
import uuid
from typing import Self, ClassVar

from asgiref.sync import sync_to_async
from django.db import models


def uuid_generate_v1mc() -> uuid.UUID:
    """Return a version 1 UUID with a random node MAC address.

    Timestamp locality + randomness provide useful properties for indexing.

    Further reading on why this is a somewhat good idea:
     - https://www.postgresql.org/docs/current/uuid-ossp.html
     - https://www.edgedb.com/docs/stdlib/uuid#function::std::uuid_generate_v1mc
    - https://datatracker.ietf.org/doc/html/draft-peabody-dispatch-new-uuid-format-04

    Further reading on why uuid V4 is probably not the best idea:
    - https://www.edgedb.com/docs/stdlib/uuid#function::std::uuid_generate_v4
    """
    from uuid import _random_getnode

    return uuid.uuid1(node=_random_getnode())


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
            deleted_at__isnull=False,
        )


class DbBaseModel(models.Model):
    """All App models should inherit from this class.

    This class provides the following features:
    - uuid primary key. Read More:
        - https://www.postgresql.org/docs/current/uuid-ossp.html#UUID-OSSP-FUNCTIONS-SECT
        -

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
