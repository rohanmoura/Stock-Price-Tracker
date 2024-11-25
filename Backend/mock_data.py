from models import StockPrice
from database import Session
import random
from datetime import datetime, timedelta 
import logging


STOCKS = [
    {
        "id": 1,
        "symbol": "AAPL",
        "current_price": 150.23,
        "timestamp": "2024-11-21 12:00:00",
        "historical_prices": [
            {"price": 148.50, "timestamp": "2024-11-20 12:00:00"},
            {"price": 149.75, "timestamp": "2024-11-19 12:00:00"},
            {"price": 147.60, "timestamp": "2024-11-18 12:00:00"},
            {"price": 146.80, "timestamp": "2024-11-17 12:00:00"}
        ]
    },
    {
        "id": 2,
        "symbol": "GOOGL",
        "current_price": 2805.67,
        "timestamp": "2024-11-21 12:00:00",
        "historical_prices": [
            {"price": 2800.20, "timestamp": "2024-11-20 12:00:00"},
            {"price": 2810.45, "timestamp": "2024-11-19 12:00:00"},
            {"price": 2795.80, "timestamp": "2024-11-18 12:00:00"},
            {"price": 2790.30, "timestamp": "2024-11-17 12:00:00"}
        ]
    },
    {
        "id": 3,
        "symbol": "MSFT",
        "current_price": 332.15,
        "timestamp": "2024-11-21 12:00:00",
        "historical_prices": [
            {"price": 330.50, "timestamp": "2024-11-20 12:00:00"},
            {"price": 333.25, "timestamp": "2024-11-19 12:00:00"},
            {"price": 331.80, "timestamp": "2024-11-18 12:00:00"},
            {"price": 329.95, "timestamp": "2024-11-17 12:00:00"}
        ]
    },
    {
        "id": 4,
        "symbol": "TSLA",
        "current_price": 720.34,
        "timestamp": "2024-11-21 12:00:00",
        "historical_prices": [
            {"price": 718.90, "timestamp": "2024-11-20 12:00:00"},
            {"price": 722.15, "timestamp": "2024-11-19 12:00:00"},
            {"price": 719.75, "timestamp": "2024-11-18 12:00:00"},
            {"price": 717.50, "timestamp": "2024-11-17 12:00:00"}
        ]
    },
    {
        "id": 5,
        "symbol": "AMZN",
        "current_price": 3400.89,
        "timestamp": "2024-11-21 12:00:00",
        "historical_prices": [
            {"price": 3395.50, "timestamp": "2024-11-20 12:00:00"},
            {"price": 3405.25, "timestamp": "2024-11-19 12:00:00"},
            {"price": 3398.80, "timestamp": "2024-11-18 12:00:00"},
            {"price": 3390.60, "timestamp": "2024-11-17 12:00:00"}
        ]
    },
    {
        "id": 6,
        "symbol": "NFLX",
        "current_price": 490.56,
        "timestamp": "2024-11-21 12:00:00",
        "historical_prices": [
            {"price": 488.90, "timestamp": "2024-11-20 12:00:00"},
            {"price": 492.15, "timestamp": "2024-11-19 12:00:00"},
            {"price": 489.75, "timestamp": "2024-11-18 12:00:00"},
            {"price": 487.40, "timestamp": "2024-11-17 12:00:00"}
        ]
    },
    {
        "id": 7,
        "symbol": "META",
        "current_price": 310.45,
        "timestamp": "2024-11-21 12:00:00",
        "historical_prices": [
            {"price": 308.90, "timestamp": "2024-11-20 12:00:00"},
            {"price": 312.15, "timestamp": "2024-11-19 12:00:00"},
            {"price": 309.75, "timestamp": "2024-11-18 12:00:00"},
            {"price": 307.60, "timestamp": "2024-11-17 12:00:00"}
        ]
    },
]




# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_mock_data():
    """
    Database mein mock data insert karne ke liye function
    """
    session = Session()
    try:
        # Clear existing data
        session.query(StockPrice).delete()
        session.commit()
        logger.info("Cleared existing data")
        
        for stock in STOCKS:
            try:
                # Add current price
                current_price = StockPrice(
                    symbol=stock["symbol"],
                    price=stock["current_price"],
                    timestamp=datetime.strptime(stock["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    is_current=True
                )
                session.add(current_price)
                
                # Add historical prices
                for hist_price in stock["historical_prices"]:
                    historical = StockPrice(
                        symbol=stock["symbol"],
                        price=hist_price["price"],
                        timestamp=datetime.strptime(hist_price["timestamp"], "%Y-%m-%d %H:%M:%S"),
                        is_current=False
                    )
                    session.add(historical)
                
                logger.info(f"Added data for {stock['symbol']}")
                
            except Exception as e:
                logger.error(f"Error adding {stock['symbol']}: {str(e)}")
                continue
        
        session.commit()
        logger.info("Mock data generation completed successfully")
        return {"status": "success", "message": "Mock data generated successfully"}
    except Exception as e:
        session.rollback()
        logger.error(f"Error in generate_mock_data: {str(e)}")
        raise e
    finally:
        session.close()
