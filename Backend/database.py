import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import logging

logger = logging.getLogger(__name__)

# Use absolute path for SQLite database in tmp directory
db_path = "/tmp/stocks.db"
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_database():
    try:
        Base.metadata.create_all(engine)
        logger.info(f"Database created successfully at: {db_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        return False
