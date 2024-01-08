from pathlib import Path
from typing import Literal, Self, Annotated

import dj_database_url
from pydantic import SecretStr, model_validator, Field, PostgresDsn, UrlConstraints
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings

SqliteDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        host_required=False,
        allowed_schemes=[
            "sqlite",
            "sqlite3",
        ],
    ),
]


class Config(BaseSettings):
    class Config:
        env_file = ".env"
        frozen = True

    env: Literal["dev", "prod"] = "dev"
    database_url: PostgresDsn | SqliteDsn = Field(
        default="sqlite:///./db.sqlite3",
        validate_default=True,
    )

    django_prefix: str = Field(
        default="/dj",
        title="Django HTTP route prefix",
        description="""
        The prefix to mount the Django ASGI application at.
        Use empty string to mount at root.
        """,
    )
    django_secret_key: SecretStr = Field(
        default="django-insecure-j1vsi)^#1(4!6ug(k3)ooh#gdx3oh3)7lr5wwbg6_+5_#wj&(p",
        validate_default=True,
    )

    @property
    def debug(self) -> bool:
        return self.env == "dev"

    @property
    def django_allowed_hosts(self: Self) -> list[str]:
        # TODO: update to domain if / when one exists
        return ["*"]

    @property
    def django_db_config(self: Self) -> dj_database_url.DBConfig:
        return dj_database_url.config(default=str(self.database_url))

    @model_validator(mode="after")
    def _no_default_django_secret_key(self: Self) -> None:
        if not self.debug and self.django_secret_key.get_secret_value().startswith(
            "django-insecure-"
        ):
            raise ValueError("Please set DJANGO_SECRET_KEY")

    @property
    def django_root(self: Self) -> str:
        return str((Path("/") / self.django_prefix))

    @property
    def django_static(self: Self) -> str:
        return str(Path(self.django_root) / "static")
