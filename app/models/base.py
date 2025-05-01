import task, user
from app.db.base import engine, Base

Base.metadata.create_all(engine)
