from app.core.security import get_password_hash
from app.db.session import session
from app.schemas.user import UserInDB, UserInRequest


def create_new_user(data: UserInRequest):
    hashed_password = get_password_hash(data.password)
    new_user = UserInDB(email=data.email, name=data.name, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    return new_user