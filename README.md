# Asset Correlation Analyzer

A web application to analyze and visualize correlations between financial assets using historical price data.

## Features

- 📊 Calculate Pearson correlation coefficients for 8+ financial assets
- 📈 Interactive correlation heatmap visualization
- 🔄 Real-time data fetching from Yahoo Finance
- 🚀 FastAPI backend with Pydantic validation
- ⚛️ React + TypeScript frontend

## Project Structure

```
asset-correlation-analyzer/
├── server/                  # Python FastAPI backend
│   ├── api/                # API routes and models
│   ├── scripts/            # Data fetching and calculation scripts
│   ├── utils/              # Utilities (logger)
│   ├── config.py           # Configuration with Pydantic Settings
│   └── main.py             # FastAPI application
├── frontend/               # React TypeScript frontend
└── data/                    # Financial data storage

```

## Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- Virtual environment

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install Python dependencies:
```bash
cd server
pip install -r requirements.txt
```

3. Configure environment:
```bash
# Create .env file in server/
echo "DATA_DIRECTORY=/absolute/path/to/data/raw" > server/.env
```

4. Fetch data and calculate correlations:
```bash
python scripts/yahoo_finance_client.py
python scripts/correlation_calculator.py
```

5. Start FastAPI server:
```bash
cd server
uvicorn main:app --reload
```

API will be available at: http://localhost:8000

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

## Usage

1. **Fetch Data**: Run the yahoo finance client to download historical data
2. **Calculate Correlations**: Run the correlation calculator to generate the matrix
3. **Start API**: Start the FastAPI server
4. **View Results**: Open the React frontend to see the correlation heatmap

## API Endpoints

- `GET /api/correlations` - Get correlation matrix for all assets
- `GET /api/health` - Health check endpoint
- `GET /` - Root endpoint

## Technologies

- **Backend**: FastAPI, Pydantic, Pandas, yfinance
- **Frontend**: React, TypeScript, Vite
- **Data**: Yahoo Finance API

## License

MIT
