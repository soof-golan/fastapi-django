# Generated by Django 5.0 on 2023-12-16 16:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fastapi_django", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="deleted_at",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                db_default=models.Value("uuid_generate_v1mc()"),
                default=uuid.uuid1,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["id", "deleted_at"], name="user_id_deleted_at_idx"
            ),
        ),
    ]