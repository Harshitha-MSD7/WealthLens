"""Generate realistic sample financial PDFs for WealthLens demo."""
from fpdf import FPDF
import os

OUT = os.path.dirname(__file__)


def make_pdf(filename, title, sections):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_fill_color(4, 13, 26)
    pdf.set_text_color(240, 180, 41)
    pdf.cell(0, 14, title, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    for heading, body in sections:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_fill_color(230, 235, 245)
        pdf.cell(0, 9, heading, ln=True, fill=True)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, body)
        pdf.ln(4)

    pdf.output(os.path.join(OUT, filename))
    print(f"Created {filename}")


# ── 1. BNY Q1 2026 Earnings ──────────────────────────────────────────
make_pdf("BNY_Q1_2026_EarningsReport.pdf", "BNY Mellon - Q1 2026 Earnings Report", [
    ("Executive Summary",
     "BNY Mellon Corporation reported first quarter 2026 earnings per diluted share of $1.73, "
     "compared with $1.60 in Q1 2025, representing an 8.1% year-over-year increase. Total revenue "
     "of $6.26 billion exceeded the consensus analyst estimate of $6.11 billion by 2.5%. "
     "Return on common equity was 11.4%, and the Common Equity Tier 1 (CET1) ratio stood at 11.8%."),

    ("Revenue Breakdown by Segment",
     "Investment Services: $3.82B (61% of total revenue), up 5.2% YoY driven by higher fee revenue "
     "and net interest income growth. Investment and Wealth Management: $1.90B (30%), reflecting "
     "continued AUM growth of 7.3% to $2.47 trillion. Other/Corporate: $0.54B (9%). "
     "Total fee revenue grew 4.8% YoY to $4.31B."),

    ("Earnings Per Share",
     "Diluted EPS: $1.73 (Q1 2026) vs $1.60 (Q1 2025). The Board of Directors declared a quarterly "
     "cash dividend of $0.47 per common share, payable May 10, 2026. Full-year 2026 EPS guidance "
     "is raised to $6.90-$7.10, up from prior guidance of $6.70-$6.90."),

    ("Liquidity Position",
     "BNY Mellon maintained a Liquidity Coverage Ratio (LCR) of 132%, well above the regulatory "
     "minimum of 100%. High-quality liquid assets (HQLA) totaled $148.6 billion. The Net Stable "
     "Funding Ratio (NSFR) was 119%. Cash and liquid equivalents on hand: $22.4 billion. "
     "The firm issued $3.0 billion in long-term debt during the quarter."),

    ("Capital & Risk",
     "Common Equity Tier 1 capital ratio: 11.8% (above the 10.5% internal target). Total capital "
     "ratio: 14.2%. Risk-weighted assets: $148.3 billion. Average assets under custody/administration "
     "reached a record $52.1 trillion, up 8% YoY. Provision for credit losses: $45 million."),

    ("Outlook",
     "Management expects full-year 2026 net interest income growth of 4-6% and fee revenue growth "
     "of 3-5%. Expense growth is targeted at 2-3% as the firm benefits from operational efficiency "
     "initiatives. The macroeconomic environment remains supportive with two anticipated Federal "
     "Reserve rate cuts in the second half of 2026."),
])

# ── 2. MSFT 10-K ─────────────────────────────────────────────────────
make_pdf("MSFT_10K_FY2025_Filing.pdf", "Microsoft Corporation - 10-K Annual Report FY2025", [
    ("Business Overview",
     "Microsoft Corporation is a technology company that develops and supports software, services, "
     "devices, and solutions. For fiscal year 2025, Microsoft reported total revenue of $261.8 billion, "
     "up 16% year-over-year. Operating income was $109.4 billion (42% margin). The company employs "
     "approximately 228,000 people worldwide."),

    ("Revenue by Segment",
     "Intelligent Cloud (Azure): $135.7B (+22% YoY) - Azure contributed 43% of total revenue, "
     "with Azure growth of 28% in constant currency. Productivity and Business Processes (Office, "
     "LinkedIn): $83.4B (+12% YoY). More Personal Computing (Windows, Xbox, Surface): $42.7B (+6% YoY)."),

    ("Key Risk Factors",
     "1. Cybersecurity Risk: Significant exposure from AI infrastructure expansion increases attack "
     "surface. The company disclosed 3 material cybersecurity incidents in FY2025. "
     "2. Regulatory Risk: EU Digital Markets Act compliance costs estimated at $1.2 billion annually. "
     "Ongoing antitrust scrutiny in the US and EU regarding AI and cloud market concentration. "
     "3. Market Concentration: Azure contributing 43% of revenue creates single-segment dependency. "
     "4. AI Competition: Intensifying competition from Google, Amazon, and emerging AI startups "
     "could pressure margins and market share in the cloud and AI segments."),

    ("Financial Performance",
     "Net income: $88.1 billion (+18% YoY). Earnings per diluted share: $11.80. Free cash flow: "
     "$74.3 billion. The company returned $34.2 billion to shareholders through dividends ($9.7B) "
     "and share repurchases ($24.5B). Total assets: $548.0 billion. Long-term debt: $42.7 billion."),

    ("Interest Rate Sensitivity",
     "A hypothetical 100 basis point increase in interest rates would result in an estimated "
     "decrease in the fair value of the investment portfolio of approximately $1.8 billion. "
     "The company's floating rate debt exposure is approximately $8.4 billion. Duration of the "
     "fixed income portfolio is 3.2 years."),
])

# ── 3. Federal Reserve Policy Update ─────────────────────────────────
make_pdf("FederalReserve_PolicyUpdate_Mar2026.pdf", "Federal Reserve - Monetary Policy Update March 2026", [
    ("Policy Statement",
     "The Federal Open Market Committee (FOMC) decided to maintain the target range for the federal "
     "funds rate at 4-1/4 to 4-1/2 percent. The Committee will continue reducing its holdings of "
     "Treasury securities and agency debt at the current pace of $60 billion per month."),

    ("Economic Outlook",
     "Recent indicators suggest that economic activity has continued to expand at a solid pace. "
     "The unemployment rate has stabilized at 4.1%. Inflation has eased over the past year but "
     "remains somewhat elevated relative to the 2% longer-run goal. CPI stands at 2.9% YoY. "
     "Core PCE inflation is 2.7%, showing steady progress toward the 2% target."),

    ("Interest Rate Guidance",
     "The Committee anticipates that it will be appropriate to reduce the target range for the "
     "federal funds rate by 25 basis points at each of two meetings in H2 2026, contingent on "
     "inflation falling sustainably below 2.8%. Markets currently price a 72% probability of the "
     "first cut at the September 2026 meeting and an 85% probability of a second cut in December 2026."),

    ("Interest Rate Sensitivity for Fixed Income Portfolios",
     "Duration-sensitive fixed income portfolios face estimated NAV impact of -1.4% per 100 basis "
     "point parallel shift in the yield curve. The 10-year Treasury yield currently stands at 4.28%. "
     "A steepening scenario (short rates down 50bps, long rates unchanged) would benefit mortgage-backed "
     "securities and long-duration bonds by an estimated 1.8-2.2% in total return."),

    ("Financial Stability Assessment",
     "Overall financial stability vulnerabilities remain moderate. Asset valuations in equity markets "
     "appear elevated relative to historical norms. Commercial real estate exposures at regional banks "
     "continue to require monitoring. Leverage in the non-bank financial sector remains elevated. "
     "Liquidity in Treasury markets has improved relative to Q4 2025."),
])

# ── 4. Portfolio Risk Assessment ─────────────────────────────────────
make_pdf("PortfolioRiskAssessment_Apr2026.pdf", "WealthLens Portfolio Risk Assessment - April 2026", [
    ("Portfolio Summary",
     "Total Assets Under Management: $2.47 billion across 8 primary positions. "
     "Portfolio risk score: 6.8/10 (Moderate-High). YTD return: +11.4% vs benchmark +8.1%. "
     "Portfolio beta: 1.12. Annualized volatility: 14.2%. Sharpe ratio: 1.42. Sortino ratio: 1.78."),

    ("Value at Risk Analysis",
     "1-Day VaR at 95% confidence: -$18.3 million (-0.74% of AUM). "
     "1-Day VaR at 99% confidence: -$26.1 million (-1.06% of AUM). "
     "Expected Shortfall (CVaR) at 95%: -$32.7 million. "
     "10-Day VaR at 99% (Basel III): -$82.5 million. "
     "Monte Carlo simulation (5,000 paths) confirms parametric VaR estimates within 3% tolerance."),

    ("Risk Factor Decomposition",
     "Market Risk: 7.8/10 - Elevated equity exposure (Technology 26.6%) drives market beta. "
     "Credit Risk: 5.2/10 - Investment grade fixed income holdings (TLT 8.7% weight). "
     "Liquidity Risk: 3.8/10 - 94% of portfolio in liquid exchange-traded securities. "
     "Concentration Risk: 7.0/10 - Top 3 positions (MSFT 14.2%, BLK 11.8%, JPM 10.5%) = 36.5% of AUM. "
     "ESG Score: 6.2/10 - Weighted average ESG rating of BBB across portfolio."),

    ("Top Holdings",
     "MSFT (14.2%, $351M): High risk, Hold signal. Azure growth slowdown flagged as key risk. "
     "BLK (11.8%, $291M): Medium risk, Buy signal. Record AUM inflows support upside. "
     "JPM (10.5%, $260M): Medium risk, Buy signal. Strong capital ratios and dividend growth. "
     "GS (9.3%, $230M): High risk, Hold signal. M&A pipeline acceleration is positive catalyst. "
     "TLT (8.7%, $215M): Low risk, Buy signal. Rate cut expectations support duration exposure."),

    ("Stress Test Results",
     "2008 Financial Crisis scenario: Estimated portfolio drawdown -34.2%. "
     "COVID-19 March 2020 scenario: Estimated portfolio drawdown -28.7%. "
     "Rising rates +200bps scenario: Estimated impact -6.4% (fixed income drag). "
     "Tech sector correction -30% scenario: Estimated impact -8.0% (26.6% tech weight). "
     "All stress scenarios show portfolio recovery within 18 months based on historical precedent."),
])

print("\nAll 4 PDFs generated successfully in sample_docs/")
