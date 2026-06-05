from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DataQuality(str, Enum):
    LIVE = "live"
    SAMPLE = "sample"
    UNAVAILABLE = "unavailable"


class SourceRecord(BaseModel):
    name: str
    url: str | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    quality: DataQuality = DataQuality.LIVE
    notes: str | None = None


class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticker: str
    source: SourceRecord

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("ticker is required")
        return value


class CompanyProfile(ToolResult):
    company_name: str | None = None
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    website: str | None = None
    cik: str | None = None
    business_summary: str | None = None


class MarketSnapshot(ToolResult):
    currency: str | None = None
    previous_close: float | None = None
    regular_market_price: float | None = None
    market_cap: float | None = None
    trailing_pe: float | None = None
    forward_pe: float | None = None
    price_to_sales: float | None = None
    fifty_two_week_low: float | None = None
    fifty_two_week_high: float | None = None
    average_volume: float | None = None


class FinancialMetrics(ToolResult):
    fiscal_period: str | None = None
    revenue: float | None = None
    gross_profit: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    diluted_eps: float | None = None
    operating_cash_flow: float | None = None
    capital_expenditure: float | None = None
    free_cash_flow: float | None = None
    cash_and_equivalents: float | None = None
    total_debt: float | None = None


class FilingFact(BaseModel):
    concept: str
    value: float | str | None
    unit: str | None = None
    fiscal_year: int | None = None
    fiscal_period: str | None = None
    form: str | None = None
    filed: str | None = None
    accession_number: str | None = None


class FilingFacts(ToolResult):
    cik: str | None = None
    facts: list[FilingFact] = Field(default_factory=list)


class NewsItem(BaseModel):
    title: str
    publisher: str | None = None
    url: str | None = None
    published_at: datetime | None = None
    summary: str | None = None


class NewsSearchResult(ToolResult):
    query: str
    items: list[NewsItem] = Field(default_factory=list)


class TickerDataBundle(BaseModel):
    ticker: str
    company_profile: CompanyProfile
    market_snapshot: MarketSnapshot
    financial_metrics: FinancialMetrics
    filing_facts: FilingFacts

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)
