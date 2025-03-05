import redis
from typing import Optional
import json
from datetime import timedelta

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str) -> Optional[dict]:
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value: dict, ttl: int = 3600) -> None:
        self.redis.setex(key, timedelta(seconds=ttl), json.dumps(value))

    def delete(self, key: str) -> None:
        self.redis.delete(key)