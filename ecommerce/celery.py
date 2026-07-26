import os
from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

app = Celery('ecommerce')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


CELERY_BEAT_SCHEDULE = {

    'generate_payouts': {
        'task': 'core.tasks.generate_payouts',
        'schedule': crontab(hour='23', minute='59'),

    },
}