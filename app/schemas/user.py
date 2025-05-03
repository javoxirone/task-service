from pydantic import BaseModel





class User(BaseModel):
    email: str | None = None
    name: str | None = None


class UserInDB(User):
    id: int
    hashed_password: str


class UserInRequest(User):
    password: str