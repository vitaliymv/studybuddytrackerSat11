import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studybuddytracker.settings")
app = Celery("studybuddytracker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()