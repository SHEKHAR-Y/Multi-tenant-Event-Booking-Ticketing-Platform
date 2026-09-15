from fastapi import Request, status
from fastapi.exceptions import HTTPException 
from app.core.redis_client import redis_client

def rate_limit(requests: int, window_seconds: int):
    def limiter(request: Request):
        client_ip = request.client.host

        # this needs to be atomic therefore use LUA script later for now this is for learning purpouse
        key = f"rate_limit:{client_ip}:{request.url.path}"
        current_count = redis_client.incr(key)

        if current_count == 1:
            redis_client.expire(key, window_seconds)

        if current_count > requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="too many requests"
            )

    return limiter