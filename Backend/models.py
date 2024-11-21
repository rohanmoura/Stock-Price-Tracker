from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockPrice(Base):
    __tablename__ = 'stock_prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, index=True)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_current = Column(Boolean, default=False)

    def __repr__(self):
        return f"<StockPrice(symbol='{self.symbol}', price={self.price}, timestamp={self.timestamp})>"
