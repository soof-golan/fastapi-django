from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from config.config import Config


@pytest.fixture()
def client() -> Iterator[TestClient]:
    from fastapi_django.main import app

    yield TestClient(app)


@pytest.fixture()
def config() -> Iterator[Config]:
    from config.config import Config

    yield Config()


def test_django_reachable(client: TestClient, config: Config):
    admin_path = Path(config.django_root) / "admin"
    response = client.get(str(admin_path))
    assert response.status_code == 200


def test_django_not_found(client: TestClient, config: Config):
    does_not_exist = Path(config.django_root) / "does-not-exist"
    response = client.get(str(does_not_exist))
    assert response.status_code == 404


def test_django_static_files(client: TestClient, config: Config):
    static_file = Path(config.django_root) / "static" / "admin" / "css" / "base.css"
    response = client.get(str(static_file))
    assert response.status_code == 200
