import redis.asyncio
from core.config import app_settings


redis = redis.asyncio.from_url(
    f"redis://:{app_settings.redis_requiredpass}@redis:{app_settings.redis_port}", decode_responses=True
)
