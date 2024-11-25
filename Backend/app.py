from flask import Flask, jsonify
from flask_cors import CORS
from models import StockPrice
from database import Session, create_database
from mock_data import generate_mock_data
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins for now
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def initialize_database():
    try:
        create_database()
        session = Session()
        stock_count = session.query(StockPrice).count()
        
        if stock_count == 0:
            logger.info("No stocks found, generating mock data...")
            generate_mock_data()
            logger.info("Mock data generation completed")
        
        session.close()
        return True
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise e

@app.route('/api/stock-price/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    logger.info(f"Received request for symbol: {symbol}")
    symbol = symbol.upper()
    
    try:
        session = Session()
        logger.info("Database session created")
        
        # Auto-initialize if empty
        count = session.query(StockPrice).count()
        logger.info(f"Current record count: {count}")
        
        if count == 0:
            logger.info("Initializing database...")
            initialize_database()
            logger.info("Database initialized")
        
        current_price = session.query(StockPrice)\
            .filter(StockPrice.symbol == symbol, StockPrice.is_current == True)\
            .first()
        
        logger.info(f"Current price query result: {current_price}")
        
        if not current_price:
            return jsonify({"error": f"Stock {symbol} not found"}), 404
            
        historical_prices = session.query(StockPrice)\
            .filter(StockPrice.symbol == symbol, StockPrice.is_current == False)\
            .order_by(StockPrice.timestamp.desc())\
            .limit(5)\
            .all()
        
        logger.info(f"Historical prices count: {len(historical_prices)}")
        
        response_data = {
            "id": current_price.id,
            "symbol": symbol,
            "current_price": current_price.price,
            "timestamp": current_price.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "historical_prices": [
                {
                    "price": price.price,
                    "timestamp": price.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
                for price in historical_prices
            ]
        }
        
        session.close()
        logger.info("Successfully processed request")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Detailed error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    try:
        logger.info("Initializing application...")
        initialize_database()
        logger.info("Database initialization completed")
        
        port = int(os.getenv('PORT', 10000))
        logger.info(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port)
        
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
