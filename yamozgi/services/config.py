import redis
from django.conf import settings
from typing import Optional


class Singleton(type):
    """
    Метакласс. Любой класс с metaclass=Singleton будет иметь только один экземпляр.
    """
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    """
    Singleton-обёртка над redis.Redis с ConnectionPool.
    Инициализация ленивa: реальное соединение создаётся при первом обращении к .conn.
    """

    def __init__(self, url: Optional[str] = None, max_connections: int = 10, decode_responses: bool = True):
        """
        :param url: строка подключения, по умолчанию берётся из settings.REDIS_URL
        :param max_connections: максимальное число соединений в пуле
        :param decode_responses: возвращать строки (а не bytes)
        """
        self.url = url or getattr(settings, "REDIS_URL")
        self.max_connections = max_connections
        self.decode_responses = decode_responses

        self.pool = redis.ConnectionPool.from_url(
            self.url,
            max_connections=self.max_connections,
            decode_responses=self.decode_responses,
        )
        self._client: Optional[redis.Redis] = None

    @property
    def conn(self) -> redis.Redis:
        """
        Возвращает redis.Redis (лениво создаётся и кэшируется).
        Используйте .conn для выполнения команд: RedisClient().conn.get(...)
        """
        if self._client is None:
            self._client = redis.Redis(connection_pool=self.pool)
        return self._client

    def ping(self) -> bool:
        """Проверка соединения."""
        return self.conn.ping()

    def close(self) -> None:
        try:
            self.pool.disconnect()
        except Exception:
            pass