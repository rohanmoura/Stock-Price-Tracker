import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Stock Price Tracker',
  description: 'Track real-time stock prices',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
