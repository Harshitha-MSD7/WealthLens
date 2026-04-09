# WealthLens — Financial Document Intelligence Platform

A full-stack financial intelligence dashboard built for asset and wealth management workflows. Upload financial documents (10-Ks, earnings reports, Fed policy briefs), ask natural language questions via a RAG pipeline, and monitor portfolio risk in real time.

---

## Features

**Document Intelligence (RAG)**
- Upload PDF, CSV, TXT, or Excel files
- LangChain pipeline: PDF → chunked embeddings → ChromaDB vector store
- GPT-4 Turbo answers questions with source citations
- Semantic search across all indexed documents

**Risk Dashboard**
- Value at Risk (VaR 95% / 99%), Expected Shortfall, Sharpe & Sortino ratios
- Multi-factor risk scoring (Market, Credit, Liquidity, Operational, Concentration)
- Monte Carlo return distribution (5,000 simulations)
- Max drawdown, beta, LCR, NSFR

**Portfolio Analytics**
- Holdings table with live price simulation, weight bars, risk badges, and Buy/Hold/Sell signals
- Asset allocation donut chart by sector
- Portfolio vs benchmark performance line chart (1M / 3M / YTD / 1Y)

**Market Sentiment**
- Live headlines via NewsAPI (optional)
- Keyword-based financial sentiment classifier (Bullish / Bearish / Neutral)
- Per-ticker sentiment scoring

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML · CSS · JavaScript · Chart.js |
| Backend | Python · FastAPI · Uvicorn |
| AI / RAG | LangChain · OpenAI GPT-4 Turbo · ChromaDB |
| Embeddings | OpenAI `text-embedding-3-small` |
| Risk Engine | NumPy · SciPy |
| Sentiment | NewsAPI · Keyword classifier |

---

## Project Structure

```
WealthLens/
├── index.html                    # Frontend dashboard
├── .gitignore
└── backend/
    ├── main.py                   # FastAPI app entry point
    ├── requirements.txt
    ├── .env.example
    ├── routers/
    │   ├── documents.py          # POST /upload, POST /query, GET /list
    │   ├── portfolio.py          # GET /metrics, /holdings, /risk, /performance
    │   └── sentiment.py          # GET /feed, GET /score/{ticker}
    └── services/
        ├── rag_service.py        # LangChain + ChromaDB RAG pipeline
        ├── risk_service.py       # NumPy VaR, Sharpe, Monte Carlo
        └── sentiment_service.py  # NewsAPI + sentiment classifier
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Harshitha-MSD7/WealthLens.git
cd WealthLens
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and add your keys:

```env
OPENAI_API_KEY=sk-...        # Required for RAG queries
NEWSAPI_KEY=                 # Optional — enables live news headlines
```

Get an OpenAI API key at [platform.openai.com](https://platform.openai.com/api-keys)
Get a free NewsAPI key at [newsapi.org](https://newsapi.org)

### 4. Start the backend

```bash
uvicorn main:app --reload
# API running at http://localhost:8000
# Docs at      http://localhost:8000/docs
```

### 5. Open the frontend

Open `index.html` directly in a browser, or serve it via the backend at `http://localhost:8000`.

> **Offline demo mode** — the frontend works without the backend running. All charts and data fall back to realistic simulated values automatically.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/documents/upload` | Upload and index a document |
| `POST` | `/api/documents/query` | RAG query across indexed docs |
| `GET` | `/api/documents/list` | List all indexed documents |
| `GET` | `/api/portfolio/metrics` | Top-level KPI cards |
| `GET` | `/api/portfolio/holdings` | Portfolio holdings list |
| `GET` | `/api/portfolio/risk` | Full risk breakdown |
| `GET` | `/api/portfolio/performance` | Time-series performance data |
| `GET` | `/api/portfolio/montecarlo` | Monte Carlo distribution |
| `GET` | `/api/sentiment/feed` | News sentiment feed |
| `GET` | `/api/sentiment/score/{ticker}` | Per-ticker sentiment score |

Interactive API docs available at `http://localhost:8000/docs` when the server is running.

---

## Inspiration

Built to mirror workflows in BNY Mellon's Asset & Wealth Management division — combining document intelligence, quantitative risk modeling, and real-time portfolio analytics in a single platform.
