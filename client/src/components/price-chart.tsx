'use client'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

interface StockData {
    current_price: number;
    timestamp: string;
    historical_prices: Array<{
        price: number;
        timestamp: string;
    }>;
}

interface PriceChartProps {
    data: StockData;
}

export function PriceChart({ data }: PriceChartProps) {
    const chartData = [
        { price: data.current_price, timestamp: data.timestamp },
        ...data.historical_prices
    ].reverse()

    return (
        <Card>
            <CardHeader>
                <CardTitle>Price History</CardTitle>
            </CardHeader>
            <CardContent className="w-full h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                        <XAxis
                            dataKey="timestamp"
                            tickFormatter={(tick) => new Date(tick).toLocaleDateString()}
                        />
                        <YAxis 
                            domain={['auto', 'auto']}
                            tickFormatter={(value) => `$${value}`}
                        />
                        <Tooltip
                            labelFormatter={(label) => new Date(label).toLocaleString()}
                            formatter={(value: number) => [`$${value.toFixed(2)}`, "Price"]}
                        />
                        <Line 
                            type="monotone" 
                            dataKey="price" 
                            stroke="#8884d8"
                            strokeWidth={2}
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    )
}
