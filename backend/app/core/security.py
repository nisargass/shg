from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
import bcrypt
import jwt
from app.core.config import settings


def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a bcrypt hashed password."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(subject: Union[str, Any], role: str, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token with user id and role."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "iat": datetime.now(timezone.utc)
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates a JWT access token, supporting demo tokens for seamless UI integration."""
    if not token:
        return None
    if token.startswith("demo-jwt-token-") and settings.ENV.lower() not in {"production", "prod"}:
        role_map = {
            "leader": ("8", "SHG_LEADER"),
            "shg_leader": ("8", "SHG_LEADER"),
            "member": ("9", "SHG_MEMBER"),
            "shg_member": ("9", "SHG_MEMBER"),
            "buyer": ("15", "BUYER"),
            "federation": ("16", "FEDERATION_OFFICER"),
            "federation_officer": ("16", "FEDERATION_OFFICER"),
            "customer": ("17", "CUSTOMER")
        }
        role_key = token.replace("demo-jwt-token-", "").lower()
        sub, role = role_map.get(role_key, ("8", "SHG_LEADER"))
        return {
            "sub": sub,
            "role": role,
            "exp": (datetime.now(timezone.utc) + timedelta(days=7)).timestamp()
        }
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
