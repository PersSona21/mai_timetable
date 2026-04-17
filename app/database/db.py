from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

DATABASE_URL = "sqlite:///db.sqlite3"  # пока SQLite

engine = create_engine(DATABASE_URL)


Session = sessionmaker(bind=engine)
session = Session()