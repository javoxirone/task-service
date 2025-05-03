import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'), echo=True)

Base = declarative_base()

