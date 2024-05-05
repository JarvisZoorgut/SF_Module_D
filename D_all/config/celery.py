import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
 
app = Celery('config')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_morning_8am': {
        'task': 'newsportal.tasks.notify_subscribers_about_weekly_news',
        'schedule': crontab(hour=13, minute=2, day_of_week='thursday'),
    },
    # 'print_every_10_seconds': {
    #     'task': 'store.tasks.printer',
    #     'schedule': 10,
    #     'args': (5,),
    # },
    #     'clear_board_every_minute': {
    #     'task': 'mc_board.tasks.clear_old',
    #     'schedule': crontab(),
    # },
    # 'action_every_monday_8am': {
    #     'task': 'action',
    #     'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    #     'args': (agrs),
    # },
}

