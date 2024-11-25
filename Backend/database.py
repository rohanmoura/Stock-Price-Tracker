from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

DATABASE_URL = "sqlite:///./stocks.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_database():
    try:
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
