"""register models to be accessible in the Django Admin app."""
import os

from django.apps import apps
from django.contrib import admin

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_stuff.django_settings")

for model in apps.get_app_config("fastapi_django").get_models():
    admin.site.register(model)
