import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

# app.conf.beat_schedule = {
#     'every': {
#         'task': 'backend.apps.users.tasks.repeat_order_make',
#         'schedule': crontab(),
#     }
# }
