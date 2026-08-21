from pwdlib import PasswordHash

from datetime import datetime, timedelta, timezone
import uuid
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.exceptions import InvalidTokenError, TokenExpiredError

from app.core.config import get_settings

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

settings = get_settings()

password_hasher = PasswordHash.recommended()

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
        "jti": str(uuid.uuid4)
    }

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algo)
    return encoded_jwt

# decode signed token
def decode_access_token(token: str)-> dict:
    ... 
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

