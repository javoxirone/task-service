from fastapi import APIRouter
from app.crud.user import create_new_user
from app.schemas.user import UserInRequest, UserInLogin

router = APIRouter()


@router.post("/register")
async def register(user: UserInRequest):
    print(user)
    new_user = create_new_user(user)
    print(new_user)
    return {"message": "User created successfully"}


@router.post("/login")
async def login(user: UserInLogin):
    print(user)
    return {"message": "User logged in successfully"}


@router.post("/refresh")
async def get_user():
    return {"message": "User details"}
