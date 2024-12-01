"""
This file contains all the celery configurations
"""

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wemessage.settings")

app = Celery("wemessage")

app.conf.update(
    broker_url=os.environ["CELERY_BROKER_URL"],
    result_backend=os.environ["CELERY_RESULT_BACKEND"],
    accept_content=["json", "pickle"],
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
