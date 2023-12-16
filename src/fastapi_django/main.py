from contextlib import asynccontextmanager
from importlib.util import find_spec
from pathlib import Path
from typing import TypedDict, AsyncIterator

from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles

from core.config import Config
from fastapi_django_admin.asgi import application as django_application

config = Config()


class State(TypedDict):
    fake_db: dict[str, str]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[State]:
    yield {
        "fake_db": {
            "1": "one",
            "2": "two",
        }
    }


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


app = FastAPI(lifespan=lifespan, debug=config.debug)
app.include_router(router)

# A hack to serve the Django admin static files without having to run collectstatic as part of the build process.
# For now, I'm not using this.
# app.mount(
#     "/static",
#     StaticFiles(
#         directory=Path(find_spec("django.contrib.admin").origin).resolve().parent
#         / "static"
#     ),
#     name="static",
# )

# Django will pick up any unmatched routes that are not handled by FastAPI routers.
# Alternatively, if you don't want collisions, mount it at a sub path,
# e.g.: /dj or /django, whatever...
app.mount("/", app=django_application)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_django.main:app", reload=True)
