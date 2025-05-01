from fastapi import APIRouter

from app.core.security import refresh_access_token
from app.crud.user import create_new_user, authenticate_user
from app.schemas.user import UserInRequest, UserInLogin, RefreshToken

router = APIRouter()


@router.post("/register")
async def register(user: UserInRequest):
    new_user = create_new_user(user)
    return {"message": "User created successfully"}


@router.post("/login")
async def login(user: UserInLogin):
    tokens = authenticate_user(user)
    return tokens


@router.post("/refresh")
async def get_user(token: RefreshToken):
    new_token = refresh_access_token(token.refresh)
    return new_token
