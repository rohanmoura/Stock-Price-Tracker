from flask import Flask, jsonify
from flask_cors import CORS
from models import StockPrice
from database import Session, create_database
from mock_data import generate_mock_data
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def initialize_database():
    try:
        create_database()
        generate_mock_data()
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False

# Initialize database on startup
initialize_database()

@app.before_request
def before_request():
    try:
        session = Session()
        count = session.query(StockPrice).count()
        if count == 0:
            create_database()
            generate_mock_data()
        session.close()
    except:
        create_database()
        generate_mock_data()

@app.route('/api/stock-price/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    symbol = symbol.upper()
    try:
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
        
        session.close()
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)