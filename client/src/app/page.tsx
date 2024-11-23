'use client'

import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { StockCard } from '@/components/stock-card'
import { PriceChart } from '@/components/price-chart'
import { HistoryTable } from '@/components/history-table'
import { getStockPrice } from '@/lib/api'

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

export default function SimplifiedStockViewer() {
  const [searchTerm, setSearchTerm] = useState('')
  const [currentStock, setCurrentStock] = useState<StockData | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async () => {
    if (!searchTerm) {
      setError('Please enter a stock symbol first!');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('Searching for:', searchTerm);
      const data = await getStockPrice(searchTerm.toUpperCase());
      console.log('Received data:', data);
      setCurrentStock(data);
    } catch (err: any) {
      console.error('Search error:', err);
      setError(err.message);
      setCurrentStock(null);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="container mx-auto p-4 min-h-screen bg-gradient-to-b from-gray-100 to-gray-200">
      <h1 className="text-4xl font-bold mb-8 text-center text-gray-800">Stock Viewer</h1>
      
      <div className="flex gap-2 mb-8 justify-center">
        <Input 
          type="text" 
          placeholder="Enter stock symbol (e.g., TSLA)" 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value.toUpperCase())}
          className="max-w-sm"
          disabled={isLoading}
        />
        <Button 
          onClick={handleSearch} 
          className="bg-blue-600 hover:bg-blue-700"
          disabled={isLoading}
        >
          {isLoading ? 'Loading...' : 'Search'}
        </Button>
      </div>

      {error && (
        <div className="max-w-md mx-auto mb-8 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-center text-red-600 font-medium">{error}</p>
          {error.includes("not found") && (
            <div className="mt-2 text-center text-sm text-gray-600">
              Available stocks: AAPL, GOOGL, MSFT, TSLA, AMZN, NFLX, META
            </div>
          )}
        </div>
      )}

      {!currentStock && !error && (
        <div className="text-center text-gray-600">
          <p className="text-lg mb-2">Enter a stock symbol to view its price details</p>
          <p className="text-sm text-gray-500">
            Try popular symbols: AAPL (Apple), GOOGL (Google), TSLA (Tesla)
          </p>
        </div>
      )}

      {currentStock ? (
        <div className="space-y-8">
          <StockCard 
            symbol={currentStock.symbol}
            currentPrice={currentStock.current_price}
            timestamp={currentStock.timestamp}
          />
          <div className="grid md:grid-cols-2 gap-8">
            <PriceChart data={currentStock} />
            <HistoryTable data={currentStock} />
          </div>
        </div>
      ) : (
        <p className="text-center text-gray-600 text-lg">
          Enter a stock symbol and click Search to view prices.
        </p>
      )}
    </div>
  )
}
