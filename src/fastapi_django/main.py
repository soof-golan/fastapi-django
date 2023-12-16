from a2wsgi import WSGIMiddleware
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config.config import Config
from config.consts import PROJECT_ROOT_DIR
from django_stuff.wsgi import application as django_application
from fastapi_django.lifespan import lifespan
from fastapi_django.router import router

config = Config()


app = FastAPI(lifespan=lifespan, debug=config.debug, redirect_slashes=True)
app.include_router(router)

# Serve the Django admin static files on the correct path.
app.mount(
    config.django_static,
    StaticFiles(directory=PROJECT_ROOT_DIR / "staticfiles"),
    name="static",
)
# We use the WSGI version of django because it handles mounted prefixes better.
app.mount(config.django_root, app=WSGIMiddleware(django_application))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_django.main:app", reload=True)
