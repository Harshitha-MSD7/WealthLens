from fastapi import APIRouter
from services.risk_service import RiskService

router = APIRouter()
risk = RiskService()


@router.get("/metrics")
def get_metrics():
    """Top-level KPI cards: AUM, risk score, YTD returns, VaR."""
    return risk.get_metrics()


@router.get("/holdings")
def get_holdings():
    """Full holdings list with price, weight, risk badge, signal."""
    return risk.get_holdings()


@router.get("/risk")
def get_risk():
    """Detailed risk breakdown: factor scores, VaR, ES, Sharpe."""
    return risk.get_risk_breakdown()


@router.get("/performance")
def get_performance(period: str = "1M"):
    """Time-series portfolio vs benchmark performance."""
    return risk.get_performance(period)


@router.get("/allocation")
def get_allocation():
    """Sector/asset allocation for the donut chart."""
    return risk.get_allocation()


@router.get("/montecarlo")
def get_montecarlo(simulations: int = 5000):
    """Monte Carlo return distribution histogram data."""
    return risk.monte_carlo(simulations)
