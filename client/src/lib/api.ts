import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

interface HistoricalPrice {
  price: number;
  timestamp: string;
}

interface StockData {
  id: number;
  symbol: string;
  current_price: number;
  timestamp: string;
  historical_prices: HistoricalPrice[];
}

const ERROR_MESSAGES = {
  NOT_FOUND: (symbol: string) => 
    `Stock "${symbol}" not found! Please try with valid symbols like AAPL, GOOGL, TSLA, etc.`,
  SERVER_ERROR: 'Oops! Server error. Please try again later.',
  NETWORK_ERROR: 'No internet connection. Please check your network and try again.',
  DEFAULT: 'Something went wrong. Please try again.'
};

export async function getStockPrice(symbol: string): Promise<StockData> {
  if (!symbol) {
    throw new Error('Please enter a stock symbol first!');
  }

  try {
    const response = await axios.get<StockData>(`${API_BASE_URL}/stock-price/${symbol}`);
    return response.data;
  } catch (err: any) {
    if (err.response?.status === 404) {
      throw new Error(ERROR_MESSAGES.NOT_FOUND(symbol));
    } else if (err.response?.status === 500) {
      throw new Error(ERROR_MESSAGES.SERVER_ERROR);
    } else if (!navigator.onLine) {
      throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
    } else {
      throw new Error(ERROR_MESSAGES.DEFAULT);
    }
  }
}

export async function checkApiHealth(): Promise<boolean> {
  try {
    await axios.get(`${API_BASE_URL}/health`);
    return true;
  } catch {
    return false;
  }
}