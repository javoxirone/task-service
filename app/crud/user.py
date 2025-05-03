from fastapi import HTTPException

from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.db.session import session
from app.models.user import User
from app.schemas.auth import UserInLogin, Token
from app.schemas.user import UserInRequest, UserInDB


def get_user_by_email(email: str) -> User:
    return session.query(User.id, User.name, User.email, User.hashed_password).filter(User.email == email).first()

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
    user_in_db = get_user_by_email(data.email)

    if not verify_password(data.password, user_in_db.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    user_data = UserInDB.model_validate(user_in_db, from_attributes=True).model_dump()
    access_token = create_access_token(data=user_data)

    refresh_token = create_refresh_token(data=user_data)
    token = Token(access=access_token, refresh=refresh_token)

    return token

