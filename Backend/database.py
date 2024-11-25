import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Use absolute path for SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "stocks.db")
DATABASE_URL = f"sqlite:///{db_path}"

# Make sure database directory exists
os.makedirs(BASE_DIR, exist_ok=True)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_database():
    try:
        Base.metadata.create_all(engine)
        print("Database created successfully at:", db_path)
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
