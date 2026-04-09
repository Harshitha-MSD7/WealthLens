"""
Risk Service — NumPy/SciPy portfolio analytics

Computes:
  - Value at Risk (Historical + Parametric)
  - Expected Shortfall (CVaR)
  - Sharpe / Sortino ratio
  - Max drawdown
  - Monte Carlo return distribution
  - Multi-factor risk scores
"""

import numpy as np
from scipy import stats
import random
from datetime import datetime, timedelta


# ── Simulated holdings (replace with DB / broker API in production) ──
HOLDINGS = [
    {"ticker": "MSFT", "name": "Microsoft Corp",         "price": 412.80, "shares": 3380,  "sector": "Technology",   "risk": "high",   "signal": "Hold"},
    {"ticker": "BLK",  "name": "BlackRock Inc",           "price": 891.50, "shares": 1310,  "sector": "Financials",   "risk": "medium", "signal": "Buy"},
    {"ticker": "JPM",  "name": "JPMorgan Chase",          "price": 205.30, "shares": 5080,  "sector": "Financials",   "risk": "medium", "signal": "Buy"},
    {"ticker": "GS",   "name": "Goldman Sachs",           "price": 487.90, "shares": 1890,  "sector": "Financials",   "risk": "high",   "signal": "Hold"},
    {"ticker": "TLT",  "name": "iShares 20Y Treasury",    "price":  92.14, "shares": 9380,  "sector": "Fixed Income", "risk": "low",    "signal": "Buy"},
    {"ticker": "VTI",  "name": "Vanguard Total Market",   "price": 239.45, "shares": 3400,  "sector": "Equities ETF", "risk": "low",    "signal": "Hold"},
    {"ticker": "NVDA", "name": "NVIDIA Corp",             "price": 892.20, "shares":  820,  "sector": "Technology",   "risk": "high",   "signal": "Sell"},
    {"ticker": "GLD",  "name": "SPDR Gold Shares",        "price": 215.80, "shares": 2810,  "sector": "Commodities",  "risk": "low",    "signal": "Hold"},
]

ALLOCATION = [
    {"label": "Technology",   "pct": 26.6, "color": "#22d3ee"},
    {"label": "Financials",   "pct": 21.1, "color": "#f0b429"},
    {"label": "Fixed Income", "pct": 14.8, "color": "#3b82f6"},
    {"label": "Equities ETF", "pct":  8.2, "color": "#10b981"},
    {"label": "Commodities",  "pct":  6.1, "color": "#a855f7"},
    {"label": "Other",        "pct": 23.2, "color": "#475569"},
]

RISK_FACTORS = {
    "Market Risk":     7.8,
    "Credit Risk":     5.2,
    "Liquidity Risk":  3.8,
    "Operational":     4.5,
    "ESG Score":       6.2,
    "Concentration":   7.0,
    "Volatility":      6.5,
}

# Seed for reproducible simulations
RNG = np.random.default_rng(42)


def _fake_daily_returns(n: int = 252, mu: float = 0.0004, sigma: float = 0.012) -> np.ndarray:
    """Generate synthetic daily log-returns."""
    return RNG.normal(mu, sigma, n)


def _simulate_prices(returns: np.ndarray, start: float = 100.0) -> np.ndarray:
    return start * np.cumprod(1 + returns)


class RiskService:

    def get_metrics(self) -> dict:
        total_aum = sum(h["price"] * h["shares"] for h in HOLDINGS)
        returns = _fake_daily_returns()
        var_95 = float(np.percentile(returns, 5) * total_aum)
        ytd_return = float(np.sum(returns[:len(returns) // 2]) * 100)

        return {
            "aum": round(total_aum / 1e9, 3),
            "aum_label": f"${total_aum / 1e9:.2f}B",
            "aum_change_pct": 3.2,
            "risk_score": 6.8,
            "risk_label": "Moderate-High",
            "ytd_return_pct": round(ytd_return, 1),
            "benchmark_return_pct": 8.1,
            "var_95_1d": round(var_95 / 1e6, 1),
            "var_95_label": f"-${abs(var_95 / 1e6):.1f}M",
        }

    def get_holdings(self) -> list[dict]:
        total_value = sum(h["price"] * h["shares"] for h in HOLDINGS)
        result = []
        for h in HOLDINGS:
            value = h["price"] * h["shares"]
            pct_change = round(random.uniform(-2.5, 3.5), 2)
            result.append({
                "ticker":  h["ticker"],
                "name":    h["name"],
                "price":   f"${h['price']:.2f}",
                "price_raw": h["price"],
                "change":  f"{'+' if pct_change >= 0 else ''}{pct_change}%",
                "change_up": pct_change >= 0,
                "weight":  round(value / total_value * 100, 1),
                "value":   round(value, 2),
                "risk":    h["risk"],
                "signal":  h["signal"],
                "sector":  h["sector"],
            })
        return sorted(result, key=lambda x: x["weight"], reverse=True)

    def get_risk_breakdown(self) -> dict:
        returns = _fake_daily_returns()
        total_aum = sum(h["price"] * h["shares"] for h in HOLDINGS)
        sorted_returns = np.sort(returns)

        var_95 = float(np.percentile(returns, 5) * total_aum)
        var_99 = float(np.percentile(returns, 1) * total_aum)
        es_95  = float(sorted_returns[sorted_returns <= np.percentile(returns, 5)].mean() * total_aum)

        annual_return = float(np.mean(returns) * 252)
        annual_vol    = float(np.std(returns) * np.sqrt(252))
        risk_free     = 0.045
        sharpe        = round((annual_return - risk_free) / annual_vol, 2)
        sortino_downside = float(np.std(returns[returns < 0]) * np.sqrt(252))
        sortino       = round((annual_return - risk_free) / sortino_downside, 2)

        prices = _simulate_prices(returns)
        peak   = np.maximum.accumulate(prices)
        drawdown = (prices - peak) / peak
        max_dd = round(float(drawdown.min()) * 100, 2)

        return {
            "factors": RISK_FACTORS,
            "overall_score": 6.8,
            "var_95_1d":   round(var_95 / 1e6, 1),
            "var_99_1d":   round(var_99 / 1e6, 1),
            "expected_shortfall": round(es_95 / 1e6, 1),
            "sharpe_ratio":  sharpe,
            "sortino_ratio": sortino,
            "annual_vol_pct": round(annual_vol * 100, 2),
            "max_drawdown_pct": max_dd,
            "beta": 1.12,
            "lcr_pct": 132,
            "nsfr_pct": 119,
        }

    def get_performance(self, period: str = "1M") -> dict:
        days_map = {"1M": 22, "3M": 66, "YTD": 68, "1Y": 252}
        n = days_map.get(period, 22)

        port_returns  = _fake_daily_returns(n, mu=0.0006, sigma=0.011)
        bench_returns = _fake_daily_returns(n, mu=0.0004, sigma=0.010)

        port_cumulative  = (np.cumprod(1 + port_returns) - 1) * 100
        bench_cumulative = (np.cumprod(1 + bench_returns) - 1) * 100

        today = datetime.today()
        labels = [(today - timedelta(days=n - i)).strftime("%b %d") for i in range(n)]
        # Thin to ~10 points for the chart
        step = max(1, n // 10)
        idx  = list(range(0, n, step))

        return {
            "labels":    [labels[i] for i in idx],
            "portfolio": [round(float(port_cumulative[i]), 2) for i in idx],
            "benchmark": [round(float(bench_cumulative[i]), 2) for i in idx],
            "period": period,
        }

    def get_allocation(self) -> list[dict]:
        return ALLOCATION

    def monte_carlo(self, simulations: int = 5000) -> dict:
        """Return histogram bins + counts for the MC return distribution."""
        annual_returns = RNG.normal(0.114, 0.18, simulations)
        counts, bin_edges = np.histogram(annual_returns * 100, bins=25)
        labels = [f"{(bin_edges[i] + bin_edges[i+1]) / 2:.1f}%" for i in range(len(counts))]
        colors = [
            "#f43f5e" if float(bin_edges[i]) < -8
            else "#10b981" if float(bin_edges[i]) > 8
            else "#f0b429"
            for i in range(len(counts))
        ]
        return {
            "labels":  labels,
            "counts":  counts.tolist(),
            "colors":  colors,
            "simulations": simulations,
            "mean_return_pct": round(float(annual_returns.mean() * 100), 2),
            "std_pct":         round(float(annual_returns.std() * 100), 2),
        }
