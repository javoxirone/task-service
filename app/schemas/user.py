from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    email: str | None = None
    name: str | None = None


class UserInDB(User):
    hashed_password: str


class UserInRequest(User):
    password: str

class UserInLogin(TokenData):
    password: str