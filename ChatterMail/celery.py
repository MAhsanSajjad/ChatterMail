from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default settings for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr_task_management.settings')

app = Celery('mr_task_management')

# Load settings from Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
