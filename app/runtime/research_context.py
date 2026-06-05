from __future__ import annotations

import json

from pydantic import BaseModel, Field

from app.runtime.llm import generate_with_gemini
from app.runtime.schemas import TickerDataBundle
from app.runtime.tools.news_search import search_company_news


class ChatterItem(BaseModel):
    topic: str
    summary: str
    confidence: str
    allowed_use: str


class MarketChatterReport(BaseModel):
    ticker: str
    items: list[ChatterItem] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class IndustryPositionReport(BaseModel):
    ticker: str
    sector: str | None = None
    industry: str | None = None
    position_summary: str
    industry_outlook: str
    key_drivers: list[str] = Field(default_factory=list)
    key_risks: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


def investigate_market_chatter(data: TickerDataBundle) -> MarketChatterReport:
    news = search_company_news(data.ticker)
    prompt = f"""Investigate recent market chatter and informal soft signals for {data.ticker}.

Company: {data.company_profile.company_name}
Sector: {data.company_profile.sector}
Industry: {data.company_profile.industry}
Existing news tool result: {news.model_dump_json()}

Return JSON only with this shape:
{{
  "items": [
    {{
      "topic": "...",
      "summary": "...",
      "confidence": "low|medium|high",
      "allowed_use": "..."
    }}
  ],
  "limitations": ["..."]
}}

Rules:
- Focus on market chatter, CEO/CFO comments, product rumors, policy chatter, customer/supplier signals, and recent narrative shifts.
- If using unverified or weakly sourced information, mark confidence as low.
- Never present rumors as verified facts.
- allowed_use must explain whether this can be used as background only or supporting evidence.
"""
    response = generate_with_gemini(prompt, use_google_search=True)
    if response:
        try:
            parsed = _parse_json_object(response)
            return MarketChatterReport(ticker=data.ticker, **parsed)
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    items = [
        ChatterItem(
            topic="Recent catalyst/news flow",
            summary=(
                news.items[0].summary
                if news.items
                else "No current news provider is configured in the MVP."
            ),
            confidence="low" if news.source.quality.value == "sample" else "medium",
            allowed_use="context only; do not treat as verified investment evidence",
        )
    ]
    return MarketChatterReport(
        ticker=data.ticker,
        items=items,
        limitations=[
            "MVP market chatter uses the chatter/news investigation tool output and may be sample/stub data.",
            "Unverified rumors or informal comments must not drive the final research view by themselves.",
        ],
    )


def analyze_industry_position(data: TickerDataBundle) -> IndustryPositionReport:
    profile = data.company_profile
    sector = profile.sector
    industry = profile.industry
    company = profile.company_name or data.ticker
    prompt = f"""Analyze {company}'s position in its industry and the current/future industry outlook.

Ticker: {data.ticker}
Sector: {sector}
Industry: {industry}
Business summary: {profile.business_summary}
Market cap: {data.market_snapshot.market_cap}
Trailing PE: {data.market_snapshot.trailing_pe}
Forward PE: {data.market_snapshot.forward_pe}
Price to sales: {data.market_snapshot.price_to_sales}

Return JSON only with this shape:
{{
  "sector": "...",
  "industry": "...",
  "position_summary": "...",
  "industry_outlook": "...",
  "key_drivers": ["..."],
  "key_risks": ["..."],
  "limitations": ["..."]
}}

Rules:
- Discuss the company's relative position, not just the sector label.
- Include current industry conditions and forward-looking outlook.
- Mention if conclusions require verification from external industry sources.
"""
    response = generate_with_gemini(prompt, use_google_search=True)
    if response:
        try:
            parsed = _parse_json_object(response)
            return IndustryPositionReport(ticker=data.ticker, **parsed)
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drivers = [
        "demand growth and cyclicality",
        "competitive positioning",
        "margin durability",
        "capital intensity",
    ]
    risks = [
        "valuation sensitivity",
        "competitive pressure",
        "macro or policy shocks",
        "data quality limitations in the MVP",
    ]

    return IndustryPositionReport(
        ticker=data.ticker,
        sector=sector,
        industry=industry,
        position_summary=f"{company} is categorized in {sector or 'an unknown sector'} / {industry or 'an unknown industry'} based on the company profile tool.",
        industry_outlook=(
            "The MVP does not yet call a live industry research provider. Treat this as a structured placeholder "
            "for industry trend analysis that will later be upgraded with search or paid data sources."
        ),
        key_drivers=drivers,
        key_risks=risks,
        limitations=["Industry analysis is rule-based in the MVP and should be verified with live sources later."],
    )


def _parse_json_object(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise json.JSONDecodeError("No JSON object found", cleaned, 0)
    return json.loads(cleaned[start : end + 1])
