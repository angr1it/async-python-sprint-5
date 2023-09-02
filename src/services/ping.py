import time
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from redis import Redis


def timer(func):
    @wraps(func)
    async def timer_wrapper(*args, **kwargs):
        start_time = time.time()
        if not await func(*args, **kwargs):
            return None
        end_time = time.time()
        return (end_time - start_time) * 1000

    return timer_wrapper


@timer
async def ping_db(db: AsyncSession) -> bool:
    try:
        await db.execute(text('SELECT 1'))
        return True
    except Exception:
        return False


@timer
async def ping_redis(redis: Redis) -> bool:
    try:
        return await redis.ping()
    except Exception:
        return False


async def ping(db: AsyncSession, redis: Redis) -> dict:
    redis_res = await ping_db(db=db)
    db_res = await ping_redis(redis=redis)
    return {
        "db": None if not redis_res else "{:.2f}ms".format(redis_res),
        "redis": None if not db_res else "{:.2f}ms".format(db_res)
    }
