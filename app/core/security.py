from datetime import datetime, timedelta
from typing import Optional, Union, Dict

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.schemas.auth import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a new refresh token."""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Dict[str, any]:
    """
    Verify that a token is valid and not expired.

    Args:
        token: The JWT token to verify
        token_type: The expected token type ('access' or 'refresh')

    Returns:
        The decoded token payload if valid

    Raises:
        HTTPException: If token is invalid, expired, or of wrong type
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=401,
                detail=f"Token type invalid, expected '{token_type}'"
            )

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )


def refresh_access_token(refresh_token: str) -> Token:
    """
    Generate a new access token using a valid refresh token.

    Args:
        refresh_token: The refresh token

    Returns:
        Dict containing new access and refresh tokens

    Raises:
        HTTPException: If refresh token is invalid or expired
    """
    payload = verify_token(refresh_token, "refresh")

    if "exp" in payload:
        del payload["exp"]
    if "type" in payload:
        del payload["type"]

    new_access_token = create_access_token(payload)
    new_refresh_token = create_refresh_token(payload)
    token = Token(access=new_access_token, refresh=new_refresh_token)
    return token



def check_auth(auth_header: str) -> int:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: user_id not found")
        return user_id
    except JWTError as e:
        print(f"JWT decode error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid authentication token: {str(e)}")
