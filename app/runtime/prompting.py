from __future__ import annotations

from app.runtime.research_context import IndustryPositionReport, MarketChatterReport
from app.runtime.schemas import TickerDataBundle


def build_prompt_context(
    data: TickerDataBundle,
    market_chatter: MarketChatterReport,
    industry_position: IndustryPositionReport,
) -> str:
    profile = data.company_profile
    market = data.market_snapshot
    financials = data.financial_metrics
    filing_facts = data.filing_facts.facts[:8]

    facts_text = "\n".join(
        f"- {fact.concept}: {fact.value} {fact.unit or ''} ({fact.fiscal_period or 'period unavailable'})"
        for fact in filing_facts
    ) or "- No SEC facts available."
    chatter_text = "\n".join(
        f"- {item.topic}: {item.summary} Confidence: {item.confidence}. Allowed use: {item.allowed_use}."
        for item in market_chatter.items
    ) or "- No market chatter available."
    industry_drivers = "\n".join(f"- {driver}" for driver in industry_position.key_drivers)
    industry_risks = "\n".join(f"- {risk}" for risk in industry_position.key_risks)

    return f"""Ticker: {data.ticker}

Company:
- Name: {profile.company_name}
- Sector: {profile.sector}
- Industry: {profile.industry}
- Summary: {profile.business_summary}
- Profile source quality: {profile.source.quality.value}

Market:
- Price: {market.regular_market_price} {market.currency or ""}
- Market cap: {market.market_cap}
- Trailing PE: {market.trailing_pe}
- Forward PE: {market.forward_pe}
- Price to sales: {market.price_to_sales}
- Market source quality: {market.source.quality.value}

Financials:
- Fiscal period: {financials.fiscal_period}
- Revenue: {financials.revenue}
- Net income: {financials.net_income}
- Free cash flow: {financials.free_cash_flow}
- Cash: {financials.cash_and_equivalents}
- Debt: {financials.total_debt}
- Financial source quality: {financials.source.quality.value}

SEC facts:
{facts_text}
- SEC source quality: {data.filing_facts.source.quality.value}

Market chatter / informal signal investigation:
{chatter_text}
Limitations:
{chr(10).join(f"- {item}" for item in market_chatter.limitations)}

Industry position and outlook:
- Position: {industry_position.position_summary}
- Outlook: {industry_position.industry_outlook}
Key industry drivers:
{industry_drivers}
Key industry risks:
{industry_risks}
Limitations:
{chr(10).join(f"- {item}" for item in industry_position.limitations)}
"""


def build_memo_prompt(context: str) -> str:
    return f"""You are an equity research workflow automation assistant.

Write a concise, non-personalized equity research memo from the context below.

Rules:
- Do not give personalized financial advice.
- Do not claim guaranteed returns.
- Do not recommend position sizing or trading execution.
- Clearly mention when data quality is sample or incomplete.
- Treat market chatter as low-confidence context unless verified.
- Discuss the company's industry position and industry outlook.
- Include both bull and bear considerations.
- End with a non-personalized research view: Bullish, Neutral, or Bearish.

Required sections:
1. Company Snapshot
2. Market and Financial Snapshot
3. Bull Case
4. Bear Case
5. Market Chatter and Soft Signals
6. Industry Position and Outlook
7. Key Risks and Data Limitations
8. Non-Personalized Research View

Context:
{context}
"""
