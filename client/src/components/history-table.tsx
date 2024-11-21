import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

interface HistoryTableProps {
    data: {
        historical_prices: Array<{ price: number; timestamp: string }>;
    }
}

export function HistoryTable({ data }: HistoryTableProps) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Historical Prices</CardTitle>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Date</TableHead>
                            <TableHead>Price</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.historical_prices.map((item, index) => (
                            <TableRow key={index}>
                                <TableCell>{new Date(item.timestamp).toLocaleDateString()}</TableCell>
                                <TableCell>${item.price.toFixed(2)}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
    )
}
