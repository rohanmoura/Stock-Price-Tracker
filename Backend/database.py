import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import logging

logger = logging.getLogger(__name__)

# Use in-memory SQLite database
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_database():
    try:
        Base.metadata.create_all(engine)
        logger.info("In-memory database created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        return False
