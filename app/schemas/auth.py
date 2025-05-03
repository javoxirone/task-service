from pydantic import BaseModel


class AccessToken(BaseModel):
    access: str

class RefreshToken(BaseModel):
    refresh: str

class Token(AccessToken, RefreshToken):
    pass


class TokenData(BaseModel):
    email: str | None = None


class UserInLogin(TokenData):
    password: str