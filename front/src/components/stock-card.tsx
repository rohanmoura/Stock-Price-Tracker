import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface StockCardProps {
  symbol: string;
  currentPrice: number;
  timestamp: string;
}

export function StockCard({ symbol, currentPrice, timestamp }: StockCardProps) {
  return (
    <Card className="bg-gradient-to-br from-blue-500 to-purple-600 text-white">
      <CardHeader>
        <CardTitle className="text-2xl">{symbol}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-4xl font-bold">${currentPrice.toFixed(2)}</p>
        <p className="text-sm mt-2">Last updated: {new Date(timestamp).toLocaleString()}</p>
      </CardContent>
    </Card>
  )
}
