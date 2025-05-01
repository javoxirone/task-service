from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:123456@localhost/task_service', echo=True)

Base = declarative_base()

