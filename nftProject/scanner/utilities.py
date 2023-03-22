import os

import dotenv
import redis

dotenv.load_dotenv()


class RedisClient:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=os.getenv("REDIS_HOST", "host"),
            port=os.getenv("REDIS_PORT", "6379"),
            db=0,
        )

    def set_connection(self):
        self._conn = redis.Redis(connection_pool=self.pool)

    @property
    def connection(self) -> "redis.Redis":
        if not hasattr(self, "_conn"):
            self.set_connection()
        return self._conn
