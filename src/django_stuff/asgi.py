"""
DO NOT USE

THE ASGI App does not handle mount points that are not at the "/" correctly.

(Or you could enlighten me and send a PR to fix this 😇)

ASGI config for django_stuff project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_stuff.django_settings")

application = get_asgi_application()
