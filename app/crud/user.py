from fastapi import HTTPException

from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.db.session import session
from app.models.user import User
from app.schemas.user import UserInRequest, UserInLogin, Token


def get_user_by_email(email: str) -> User:
    return session.query(User).filter(User.email == email).first()

def user_exists(email: str) -> bool:
    return bool(get_user_by_email(email))

def create_new_user(data: UserInRequest):
    if user_exists(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(data.password)
    new_user = User(
        email=data.email,
        name=data.name,
        hashed_password=hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def authenticate_user(data: UserInLogin) -> Token:
    if not verify_password(data.password, get_user_by_email(data.email).hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(data=data.__dict__)
    refresh_token = create_refresh_token(data=data.__dict__)
    token = Token(access=access_token, refresh=refresh_token)
    return token

