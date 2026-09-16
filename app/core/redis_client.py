import redis

from app.core.config import get_settings

settings = get_settings()

redis_client = redis.from_url(
    url=settings.redis_url,
    decode_responses=True
)