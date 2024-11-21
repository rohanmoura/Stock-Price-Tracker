from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./stocks.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_database():
    Base.metadata.create_all(engine)
