import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yamozgi.settings')


app = Celery('yamozgi')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Автообнаружение задач в приложениях Django
app.autodiscover_tasks()

# Настройка расписания для периодических задач (через Celery Beat)
app.conf.beat_schedule = {
    'match-users-every-5-seconds': {  # Имя задачи в расписании
        'task': 'matchmaking.tasks.match_users',  # Путь к задаче скорее всего изменится
        'schedule': 5.0,  # Запуск каждые 5 секунд
    },
}