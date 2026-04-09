"""
Sentiment Service

Uses NewsAPI for headlines (if NEWSAPI_KEY is set), then scores each
headline with a simple keyword-based classifier.

For production: swap classifier with HuggingFace
`pipeline("text-classification", model="ProsusAI/finbert")`
"""

import os
import random
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# Fallback seed articles when NewsAPI key is absent
SEED_ARTICLES = [
    {"title": "BNY Mellon beats Q1 estimates — EPS $1.73 vs $1.65 expected",      "ticker": "BK",   "hours": 2},
    {"title": "Fed signals two rate cuts in H2 2026 — bond markets rally",          "ticker": "TLT",  "hours": 4},
    {"title": "MSFT Azure growth slows to 28% — analysts revise price targets",     "ticker": "MSFT", "hours": 6},
    {"title": "NVIDIA data center demand robust despite supply chain pressure",      "ticker": "NVDA", "hours": 8},
    {"title": "Goldman Sachs upgraded to Buy — M&A pipeline accelerating in 2026",  "ticker": "GS",   "hours": 12},
    {"title": "JPMorgan raises dividend 5% citing strong capital ratios",            "ticker": "JPM",  "hours": 16},
    {"title": "Gold hits $2,200 as dollar weakens on soft CPI print",               "ticker": "GLD",  "hours": 20},
    {"title": "BlackRock AUM crosses $12T — record ETF inflows Q1",                 "ticker": "BLK",  "hours": 24},
]

# Simple finbert-style keyword rules
_BULLISH  = {"beat", "upgrade", "rally", "record", "strong", "rises", "surges", "growth",
             "dividend", "inflows", "profit", "exceeds", "robust", "positive"}
_BEARISH  = {"miss", "downgrade", "slows", "pressure", "falls", "cuts", "loss", "weak",
             "concern", "revise", "decline", "risk", "warning", "probe"}


def _classify(text: str) -> tuple[str, str]:
    tokens = set(text.lower().replace(",", "").replace(".", "").split())
    bull = len(tokens & _BULLISH)
    bear = len(tokens & _BEARISH)
    if bull > bear:
        return "Bullish", "si-bull"
    if bear > bull:
        return "Bearish", "si-bear"
    return "Neutral", "si-neut"


def _fetch_newsapi(ticker: str) -> list[dict]:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 3,
        "apiKey": NEWSAPI_KEY,
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code != 200:
            return []
        articles = resp.json().get("articles", [])
        results = []
        for art in articles:
            title = art.get("title", "")
            if not title or "[Removed]" in title:
                continue
            score, cls = _classify(title)
            published = art.get("publishedAt", "")
            source = art.get("source", {}).get("name", "News")
            results.append({
                "title":  title,
                "ticker": ticker,
                "score":  score,
                "cls":    cls,
                "source": source,
                "published_at": published,
            })
        return results
    except Exception:
        return []


class SentimentService:

    def get_feed(self, tickers: list[str]) -> list[dict]:
        articles = []

        if NEWSAPI_KEY:
            for ticker in tickers[:5]:  # limit API calls
                articles.extend(_fetch_newsapi(ticker))

        # Pad / fallback with seed articles
        if len(articles) < 5:
            for seed in SEED_ARTICLES:
                if seed["ticker"] in tickers or not articles:
                    score, cls = _classify(seed["title"])
                    pub_time = datetime.utcnow() - timedelta(hours=seed["hours"])
                    articles.append({
                        "title":  seed["title"],
                        "ticker": seed["ticker"],
                        "score":  score,
                        "cls":    cls,
                        "source": self._source_name(seed["ticker"]),
                        "published_at": pub_time.isoformat() + "Z",
                    })

        # Deduplicate and cap at 8
        seen, unique = set(), []
        for a in articles:
            if a["title"] not in seen:
                seen.add(a["title"])
                unique.append(a)
        return unique[:8]

    def get_ticker_score(self, ticker: str) -> dict:
        if NEWSAPI_KEY:
            articles = _fetch_newsapi(ticker)
        else:
            articles = [a for a in self.get_feed([ticker]) if a["ticker"] == ticker]

        if not articles:
            return {"ticker": ticker, "score": "Neutral", "articles": 0, "confidence": 0.5}

        scores = [a["score"] for a in articles]
        bull = scores.count("Bullish")
        bear = scores.count("Bearish")
        total = len(scores)
        if bull > bear:
            agg, conf = "Bullish", round(bull / total, 2)
        elif bear > bull:
            agg, conf = "Bearish", round(bear / total, 2)
        else:
            agg, conf = "Neutral", 0.5

        return {"ticker": ticker, "score": agg, "articles": total, "confidence": conf}

    @staticmethod
    def _source_name(ticker: str) -> str:
        mapping = {
            "MSFT": "WSJ", "BK": "Reuters", "JPM": "Bloomberg",
            "GS": "Barron's", "NVDA": "FT", "TLT": "Bloomberg",
            "GLD": "Reuters", "BLK": "FT",
        }
        return mapping.get(ticker, "MarketWatch")
