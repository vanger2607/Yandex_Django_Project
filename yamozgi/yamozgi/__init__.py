# Импорт Celery app для интеграции с Django
from .celery import app as celery_app
__all__ = ('celery_app',)