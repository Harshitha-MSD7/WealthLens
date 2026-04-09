from fastapi import APIRouter, Query
from services.sentiment_service import SentimentService

router = APIRouter()
svc = SentimentService()


@router.get("/feed")
def get_feed(tickers: str = Query(default="MSFT,BK,JPM,GS,NVDA,TLT,GLD")):
    ticker_list = [t.strip().upper() for t in tickers.split(",")]
    return svc.get_feed(ticker_list)


@router.get("/score/{ticker}")
def get_score(ticker: str):
    return svc.get_ticker_score(ticker.upper())
