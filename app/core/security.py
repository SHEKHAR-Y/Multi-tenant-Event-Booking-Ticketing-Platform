import uuid
from datetime import datetime, timedelta, timezone

# app/core/security.py
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import get_settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError, UserNotAuthorized


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        header_token = await super().__call__(request)  # won't raise, since auto_error=False below
        if header_token:
            return header_token
        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            return cookie_token
        raise UserNotAuthorized("not authorized")
    
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/login", auto_error=False)

settings = get_settings()

password_hasher = PasswordHash.recommended()

# hash password 
def hash_password(password: str) -> str: 
    return password_hasher.hash(password)

def verify_password(password: str, stored_hash: str) -> bool:
    return password_hasher.verify(password, stored_hash)

# create signed access token
def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    now = datetime.now(timezone.utc)
    expiry = now + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))

    to_encode = {
        "sub": subject,
        "iat": now,
        "exp": expiry,
        "jti": str(uuid.uuid4())
    }

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algo)
    return encoded_jwt

# decode signed token
def decode_access_token(token: str)-> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algo]
        )

        return payload
    except ExpiredSignatureError: 
        raise TokenExpiredError()
    except JWTError: 
        raise InvalidTokenError()

# create signed refresh token
def create_refresh_token(subject: str, expires_delta: timedelta | None = None) -> str:
    now = datetime.now(timezone.utc)
    expiry = now + (expires_delta or timedelta(days=settings.refresh_token_expire_days))
    jti = str(uuid.uuid4())
    to_encode = {
        "sub": subject,
        "iat": now,
        "exp": expiry,
        "jti": jti,
        "type": "refresh"
    }

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algo)
    return encoded_jwt, jti, expiry

# decode signed refresh token
def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algo]
        )
        if payload["type"] != "refresh":
            raise InvalidTokenError()
        return payload
    except KeyError: # becuase if someone pass a access_token instead of refresh_token then it will not have a type key in the payload  
        raise InvalidTokenError()
    except ExpiredSignatureError: 
            raise TokenExpiredError()
    except JWTError: 
            raise InvalidTokenError()