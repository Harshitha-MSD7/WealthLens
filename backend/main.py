from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from routers import documents, portfolio, sentiment

app = FastAPI(
    title="WealthLens API",
    description="Financial Document Intelligence & Risk Analytics Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(sentiment.router, prefix="/api/sentiment", tags=["Sentiment"])

# Serve the frontend
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "index.html")

@app.get("/", response_class=FileResponse)
def serve_frontend():
    return FileResponse(FRONTEND_PATH)

@app.get("/health")
def health():
    return {"status": "ok", "service": "WealthLens API"}
