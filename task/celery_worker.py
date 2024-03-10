from celery import Celery

from data.config import settings

app = Celery('task', include=['task.tasks'])
app.config_from_object('task.celeryconfig')
app.conf.beat_schedule = {
    'send-notifications': {
      'task': 'task.tasks.notify_task',
      'schedule': settings.NOTIFICATION_FREQUENCY
    }
}
