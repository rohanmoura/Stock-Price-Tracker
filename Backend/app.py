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

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)
REDIS_EXPIRATION = 300

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

port = int(os.getenv('PORT', 10000))
host = '0.0.0.0'

def initialize_database():
    db_file = "./stocks.db"
    
    if not os.path.exists(db_file):
        create_database()
        
        session = Session()
        stock_count = session.query(StockPrice).count()
        session.close()
        
        if stock_count == 0:
            generate_mock_data()

initialize_database()

@app.route('/api/stock-price/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    symbol = symbol.upper()
    
    try:
        cached_data = redis_client.get(f"stock_price:{symbol}")
        if cached_data:
            return jsonify(json.loads(cached_data))
        
        session = Session()
        current_price = session.query(StockPrice)\
            .filter(StockPrice.symbol == symbol, StockPrice.is_current == True)\
            .first()
            
        if not current_price:
            return jsonify({"error": f"Stock {symbol} not found"}), 404
            
        historical_prices = session.query(StockPrice)\
            .filter(StockPrice.symbol == symbol, StockPrice.is_current == False)\
            .order_by(StockPrice.timestamp.desc())\
            .limit(5)\
            .all()
        
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
        
        redis_client.setex(
            f"stock_price:{symbol}",
            REDIS_EXPIRATION,
            json.dumps(response_data)
        )
        
        session.close()
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    app.run(host=host, port=port, debug=False)
