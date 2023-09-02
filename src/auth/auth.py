from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
)
from fastapi_users.authentication import RedisStrategy

from core.config import app_settings
from config.redis import redis

COOKIE_MAX_AGE = 3600
COOKIE_NAME = f"{app_settings.app_title}"


cookie_transport = CookieTransport(
    cookie_name=COOKIE_NAME,
    cookie_max_age=COOKIE_MAX_AGE,
    cookie_secure=False,
)


def get_redis_strategy() -> RedisStrategy:
    yield RedisStrategy(redis, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt", transport=cookie_transport, get_strategy=get_redis_strategy
)
