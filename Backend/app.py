from flask import Flask, jsonify
from flask_cors import CORS
from models import StockPrice
from database import Session, create_database, engine
from mock_data import generate_mock_data
import os
import redis
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Redis setup
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)
REDIS_EXPIRATION = 300  # 5 minutes cache

def initialize_database():
    """
    Check if database exists and initialize if needed
    """
    db_file = "./stocks.db"
    
    if not os.path.exists(db_file):
        print("Database not found, creating new database...")
        create_database()
        
        session = Session()
        stock_count = session.query(StockPrice).count()
        session.close()
        
        if stock_count == 0:
            print("Adding mock data to database...")
            generate_mock_data()
            print("Mock data added successfully!")
    else:
        print("Database already exists!")

# Initialize database on startup
initialize_database()

@app.route('/api/stock-price/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """
    Get stock price from Redis cache or database
    """
    symbol = symbol.upper()
    
    try:
        # Check Redis cache first
        cached_data = redis_client.get(f"stock_price:{symbol}")
        if cached_data:
            print(f"Cache HIT for {symbol}")
            return jsonify(json.loads(cached_data))
        
        print(f"Cache MISS for {symbol}")
        
        # Get from database if not in cache
        session = Session()
        
        # Get current price
        current_price = session.query(StockPrice)\
            .filter(StockPrice.symbol == symbol, StockPrice.is_current == True)\
            .first()
            
        if not current_price:
            return jsonify({"error": f"Stock {symbol} not found"}), 404
            
        # Get historical prices
        historical_prices = session.query(StockPrice)\
            .filter(StockPrice.symbol == symbol, StockPrice.is_current == False)\
            .order_by(StockPrice.timestamp.desc())\
            .limit(5)\
            .all()
        
        # Prepare response data
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
        
        # Cache in Redis
        redis_client.setex(
            f"stock_price:{symbol}",
            REDIS_EXPIRATION,
            json.dumps(response_data)
        )
        
        session.close()
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    app.run(debug=True)
