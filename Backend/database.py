from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL
DATABASE_URL = "sqlite:///./stocks.db"

# Create engine
engine = create_engine(DATABASE_URL)

# Create sessionmaker
Session = sessionmaker(bind=engine)

def create_database():
    """Create all database tables"""
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
        return {"message": "Database tables created successfully"}
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        return {"error": str(e)}
