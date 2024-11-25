import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:10000';

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
    console.log('Calling API:', `${API_BASE_URL}/api/stock-price/${symbol}`);
    const response = await axios.get<StockData>(`${API_BASE_URL}/api/stock-price/${symbol}`);
    console.log('API Response:', response.data);
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      console.error('API Error Details:', {
        status: error.response?.status,
        data: error.response?.data,
        headers: error.response?.headers
      });
    }
    throw error;
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