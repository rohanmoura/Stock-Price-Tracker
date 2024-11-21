# 📈 Stock Price Tracker

A modern stock price tracking application that provides real-time stock prices and historical data visualization. Built with Next.js for the frontend and Flask for the backend, featuring Redis caching for optimal performance.

![Project Banner](./screenshots/banner.png)

## ✨ Features

### Core Features
- 🔍 Real-time stock price search
- 📊 Interactive price charts using Recharts
- 📜 Historical price data display
- ⚡ Redis caching for faster response times
- 🎯 Support for major stock symbols (AAPL, GOOGL, etc.)
- 💫 Smooth loading states and transitions
- ❌ Comprehensive error handling

### Technical Features
- 🚀 Server-side caching with Redis
- 📱 Responsive design for all devices
- 🔄 Automatic database initialization
- 🛡️ Type-safe with TypeScript
- 🎨 Modern UI with Tailwind CSS

## 🛠️ Tech Stack

### Frontend
- **Next.js 13** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Axios** - API requests
- **Shadcn UI** - UI components

### Backend
- **Flask** - Python web framework
- **SQLite** - Database
- **Redis** - Caching
- **SQLAlchemy** - ORM
- **Flask-CORS** - CORS handling

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- Redis server
- Git

### Installation Steps

1. **Clone the repository**

git clone https://github.com/your-username/stock-price-tracker.git
cd stock-price-tracker


2. **Backend Setup**

Navigate to backend directory

cd Backend

Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Start Flask server
python app.py

3. **Frontend Setup**

Navigate to frontend directory
cd frontend
Install dependencies
npm install
Start development server
npm run dev

4. **Redis Setup**
redis-server


5. **Access the Application**
- Open [http://localhost:3000](http://localhost:3000) in your browser
- Try searching for stock symbols like AAPL, GOOGL, TSLA

## 📊 Project Structure

stock-price-tracker/
├── frontend/
│ ├── src/
│ │ ├── app/
│ │ │ ├── page.tsx # Main UI component
│ │ │ └── layout.tsx # Layout wrapper
│ │ ├── components/
│ │ │ ├── stock-card.tsx # Stock info display
│ │ │ ├── price-chart.tsx # Price visualization
│ │ │ └── history-table.tsx # Historical data
│ │ └── lib/
│ │ └── api.ts # API integration
│ └── package.json
└── Backend/
├── app.py # Main Flask application
├── models.py # Database models
├── database.py # Database configuration
└── mock_data.py # Initial stock data




## 🎯 Available Stock Symbols

| Symbol | Company Name |
|--------|--------------|
| AAPL   | Apple Inc.   |
| GOOGL  | Google       |
| MSFT   | Microsoft    |
| TSLA   | Tesla        |
| AMZN   | Amazon       |
| NFLX   | Netflix      |
| META   | Meta         |

## 🖼️ Screenshots

### Stock Search and Display
![Search Interface](./screenshots/search.png)

### Price Chart
![Price Chart](./screenshots/chart.png)

### Historical Data
![Historical Data](./screenshots/history.png)

## 🔄 How It Works

1. **Frontend**:
   - User enters stock symbol
   - UI shows loading state
   - Displays data in three components:
     - Current price card
     - Interactive price chart
     - Historical price table

2. **Backend**:
   - Checks Redis cache first
   - If cache miss, queries database
   - Updates Redis cache
   - Returns data to frontend

3. **Caching**:
   - Redis stores stock data for 5 minutes
   - Improves response time
   - Reduces database load

## 🛠️ Development Process

This project was developed following these steps:

1. **Planning & Setup**:
   - Requirement analysis
   - Technology selection
   - Project structure setup

2. **Backend Development**:
   - Flask API setup
   - Database models
   - Redis integration
   - Mock data creation

3. **Frontend Development**:
   - Next.js setup
   - Component creation
   - API integration
   - UI/UX implementation

4. **Integration & Testing**:
   - API testing
   - Error handling
   - Performance optimization
   - Responsive design testing

## 📝 Learning Outcomes

- Full-stack application development
- Redis caching implementation
- Real-time data handling
- Modern UI development with Next.js
- Database management with SQLAlchemy
- API development with Flask

## 🤝 Contributing

Feel free to fork this project and make improvements. Pull requests are welcome!

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

ROHAN
- GitHub: rohanmoura(https://github.com/rohanmoura)
- LinkedIn: rohanmoura(https://www.linkedin.com/in/rohan-moura-66486527b/)

---

<p align="center">Made with ❤️ and 🧠</p>