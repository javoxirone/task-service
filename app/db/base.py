from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()

