import json
from typing import Any, Optional
from datetime import timedelta
import redis.asyncio as redis
from src.core.config import settings


class RedisManager:
    _pool: Optional[redis.ConnectionPool] = None
    _client: Optional[redis.Redis] = None

    @classmethod
    async def initialize(cls):
        cls._pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            max_connections=50,
            decode_responses=True,
        )
        cls._client = redis.Redis(connection_pool=cls._pool)

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
        if cls._pool:
            await cls._pool.disconnect()

    @classmethod
    def get_client(cls) -> redis.Redis:
        if not cls._client:
            raise RuntimeError("Redis not initialized")
        return cls._client

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        return await cls._client.get(key)

    @classmethod
    async def set(
        cls, key: str, value: Any, expire: Optional[int] = None
    ):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        if expire:
            await cls._client.setex(key, expire, value)
        else:
            await cls._client.set(key, value)

    @classmethod
    async def delete(cls, key: str):
        await cls._client.delete(key)

    @classmethod
    async def get_json(cls, key: str) -> Optional[Any]:
        data = await cls._client.get(key)
        if data:
            return json.loads(data)
        return None

    @classmethod
    async def set_json(
        cls, key: str, value: Any, expire: Optional[int] = None
    ):
        await cls.set(key, json.dumps(value), expire)

    @classmethod
    async def exists(cls, key: str) -> bool:
        return await cls._client.exists(key) > 0

    @classmethod
    async def incr(cls, key: str) -> int:
        return await cls._client.incr(key)

    @classmethod
    async def expire(cls, key: str, seconds: int):
        await cls._client.expire(key, seconds)

    @classmethod
    async def lpush(cls, key: str, *values):
        await cls._client.lpush(key, *values)

    @classmethod
    async def lrange(cls, key: str, start: int, end: int):
        return await cls._client.lrange(key, start, end)

    @classmethod
    async def publish(cls, channel: str, message: str):
        await cls._client.publish(channel, message)


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, identifier: str) -> bool:
        client = RedisManager.get_client()
        key = f"ratelimit:{identifier}"
        current = await client.get(key)

        if current is None:
            pipe = client.pipeline()
            await pipe.set(key, 1)
            await pipe.expire(key, self.window_seconds)
            await pipe.execute()
            return True

        if int(current) >= self.max_requests:
            return False

        await client.incr(key)
        return True

    async def get_remaining(self, identifier: str) -> int:
        client = RedisManager.get_client()
        key = f"ratelimit:{identifier}"
        current = await client.get(key)
        if current is None:
            return self.max_requests
        return max(0, self.max_requests - int(current))
