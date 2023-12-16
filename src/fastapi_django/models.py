from django.db import models

from fastapi_django.db.base import DbBaseModel


class User(DbBaseModel):
    firebase_id = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )
