import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweet_tracker.settings')

app = Celery('tweet_tracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_tweets': {
        'task': 'fetch_new_tweets',
        'schedule': 60,
        'options': {
            'expires': 30,
        },
    },
    'update_deleted_tweets': {
        'task': 'update_deleted_tweets',
        'schedule': crontab(hour=0, minute=0),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
