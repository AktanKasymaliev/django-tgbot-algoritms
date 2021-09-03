import os

from celery import Celery

from configurations import config

# Set the default Django settings module for the 'celery' program.
config()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('celery_config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "remind-user": {
        "task": "learn_algoritms_bot.tasks.remind",
        "schedule": 86400.0
    }
}