from pydantic import BaseModel


class AccessToken(BaseModel):
    access: str

class RefreshToken(BaseModel):
    refresh: str

class Token(AccessToken, RefreshToken):
    pass


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