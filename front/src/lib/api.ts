import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:10000';

interface StockData {
  id: number;
  symbol: string;
  current_price: number;
  timestamp: string;
  historical_prices: Array<{
    price: number;
    timestamp: string;
  }>;
}

export async function getStockPrice(symbol: string): Promise<StockData> {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/stock-price/${symbol}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 404) {
        throw new Error(`Stock ${symbol} not found`);
      }
      throw new Error('Failed to fetch stock data');
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